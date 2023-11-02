# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from email import encoders
from email.charset import Charset
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formataddr, formatdate, getaddresses, make_msgid
import logging
import re
import smtplib
import threading

import html2text

from odoo import api, fields, models, tools, _
from odoo.exceptions import except_orm, UserError
from odoo.tools import ustr, pycompat

_logger = logging.getLogger(__name__)
_test_logger = logging.getLogger('odoo.tests')

SMTP_TIMEOUT = 60


class MailDeliveryException(except_orm):
    """Specific exception subclass for mail delivery errors"""
    def __init__(self, name, value):
        super(MailDeliveryException, self).__init__(name, value)

# Python 3: patch SMTP's internal printer/debugger
def _print_debug(self, *args):
    _logger.debug(' '.join(str(a) for a in args))
smtplib.SMTP._print_debug = _print_debug

# Python 2: replace smtplib's stderr
class WriteToLogger(object):
    def write(self, s):
        _logger.debug(s)
smtplib.stderr = WriteToLogger()

def is_ascii(s):
    return all(ord(cp) < 128 for cp in s)

def encode_header(header_text):
    """Returns an appropriate representation of the given header value,
       suitable for direct assignment as a header value in an
       email.message.Message. RFC2822 assumes that headers contain
       only 7-bit characters, so we ensure it is the case, using
       RFC2047 encoding when needed.

       :param header_text: unicode or utf-8 encoded string with header value
       :rtype: string | email.header.Header
       :return: if ``header_text`` represents a plain ASCII string,
                return the same 7-bit string, otherwise returns an email.header.Header
                that will perform the appropriate RFC2047 encoding of
                non-ASCII values.
    """
    if not header_text:
        return ""
    header_text = ustr(header_text) # FIXME: require unicode higher up?
    if is_ascii(header_text):
        return pycompat.to_text(header_text)
    return Header(header_text, 'utf-8')

def encode_header_param(param_text):
    """Returns an appropriate RFC2047 encoded representation of the given
       header parameter value, suitable for direct assignation as the
       param value (e.g. via Message.set_param() or Message.add_header())
       RFC2822 assumes that headers contain only 7-bit characters,
       so we ensure it is the case, using RFC2047 encoding when needed.

       :param param_text: unicode or utf-8 encoded string with header value
       :rtype: string
       :return: if ``param_text`` represents a plain ASCII string,
                return the same 7-bit string, otherwise returns an
                ASCII string containing the RFC2047 encoded text.
    """
    # For details see the encode_header() method that uses the same logic
    if not param_text:
        return ""
    param_text = ustr(param_text) # FIXME: require unicode higher up?
    if is_ascii(param_text):
        return pycompat.to_text(param_text) # TODO: is that actually necessary?
    return Charset("utf-8").header_encode(param_text)

address_pattern = re.compile(r'([^ ,<@]+@[^> ,]+)')

def extract_rfc2822_addresses(text):
    """Returns a list of valid RFC2822 addresses
       that can be found in ``source``, ignoring
       malformed ones and non-ASCII ones.
    """
    if not text:
        return []
    candidates = address_pattern.findall(ustr(text))
    return [c for c in candidates if is_ascii(c)]


def encode_rfc2822_address_header(header_text):
    """If ``header_text`` contains non-ASCII characters,
       attempts to locate patterns of the form
       ``"Name" <address@domain>`` and replace the
       ``"Name"`` portion by the RFC2047-encoded
       version, preserving the address part untouched.
    """
    def encode_addr(addr):
        name, email = addr
        # If s is a <text string>, then charset is a hint specifying the
        # character set of the characters in the string. The Unicode string
        # will be encoded using the following charsets in order: us-ascii,
        # the charset hint, utf-8. The first character set to not provoke a
        # UnicodeError is used.
        # -> always pass a text string to Header

        # also Header.__str__ in Python 3 "Returns an approximation of the
        # Header as a string, using an unlimited line length.", the old one
        # was "A synonym for Header.encode()." so call encode() directly?
        name = Header(pycompat.to_text(name)).encode()
        # if the from does not follow the (name <addr>),* convention, we might
        # try to encode meaningless strings as address, as getaddresses is naive
        # note it would also fail on real addresses with non-ascii characters
        try:
            return formataddr((name, email))
        except UnicodeEncodeError:
            _logger.warning(_('Failed to encode the address %s\n'
                              'from mail header:\n%s') % (addr, header_text))
            return ""

    addresses = getaddresses([pycompat.to_text(ustr(header_text))])
    return COMMASPACE.join(a for a in (encode_addr(addr) for addr in addresses) if a)

class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def _get_default_bounce_address(self):
        '''Compute the default bounce address.

        The default bounce address is used to set the envelop address if no
        envelop address is provided in the message.  It is formed by properly
        joining the parameters "mail.bounce.alias" and
        "mail.catchall.domain".

        If "mail.bounce.alias" is not set it defaults to "postmaster-odoo".

        If "mail.catchall.domain" is not set, return None.

        '''
        get_param = self.env['ir.config_parameter'].sudo().get_param
        postmaster = get_param('mail.bounce.alias', default='postmaster-odoo')
        domain = get_param('mail.catchall.domain')
        if postmaster and domain:
            return '%s@%s' % (postmaster, domain)

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   smtp_session=None):
        """Sends an email directly (no queuing).

        No retries are done, the caller should handle MailDeliveryException in order to ensure that
        the mail is never lost.

        If the mail_server_id is provided, sends using this mail server, ignoring other smtp_* arguments.
        If mail_server_id is None and smtp_server is None, use the default mail server (highest priority).
        If mail_server_id is None and smtp_server is not None, use the provided smtp_* arguments.
        If both mail_server_id and smtp_server are None, look for an 'smtp_server' value in server config,
        and fails if not found.

        :param message: the email.message.Message to send. The envelope sender will be extracted from the
                        ``Return-Path`` (if present), or will be set to the default bounce address.
                        The envelope recipients will be extracted from the combined list of ``To``,
                        ``CC`` and ``BCC`` headers.
        :param smtp_session: optional pre-established SMTP session. When provided,
                             overrides `mail_server_id` and all the `smtp_*` parameters.
                             Passing the matching `mail_server_id` may yield better debugging/log
                             messages. The caller is in charge of disconnecting the session.
        :param mail_server_id: optional id of ir.mail_server to use for sending. overrides other smtp_* arguments.
        :param smtp_server: optional hostname of SMTP server to use
        :param smtp_encryption: optional TLS mode, one of 'none', 'starttls' or 'ssl' (see ir.mail_server fields for explanation)
        :param smtp_port: optional SMTP port, if mail_server_id is not passed
        :param smtp_user: optional SMTP user, if mail_server_id is not passed
        :param smtp_password: optional SMTP password to use, if mail_server_id is not passed
        :param smtp_debug: optional SMTP debug flag, if mail_server_id is not passed
        :return: the Message-ID of the message that was just sent, if successfully sent, otherwise raises
                 MailDeliveryException and logs root cause.
        """
        # Use the default bounce address **only if** no Return-Path was
        # provided by caller.  Caller may be using Variable Envelope Return
        # Path (VERP) to detect no-longer valid email addresses.
        smtp_from = message['Return-Path'] or self._get_default_bounce_address() or message['From']
        assert smtp_from, "The Return-Path or From header is required for any outbound email"

        # The email's "Envelope From" (Return-Path), and all recipient addresses must only contain ASCII characters.
        from_rfc2822 = extract_rfc2822_addresses(smtp_from)
        assert from_rfc2822, ("Malformed 'Return-Path' or 'From' address: %r - "
                              "It should contain one valid plain ASCII email") % smtp_from
        # use last extracted email, to support rarities like 'Support@MyComp <support@mycompany.com>'
        smtp_from = from_rfc2822[-1]
        email_to = message['To']
        email_cc = message['Cc']
        email_bcc = message['Bcc']
        del message['Bcc']

        smtp_to_list = [
            address
            for base in [email_to, email_cc, email_bcc]
            for address in extract_rfc2822_addresses(base)
            if address
        ]
        assert smtp_to_list, self.NO_VALID_RECIPIENT

        x_forge_to = message['X-Forge-To']
        if x_forge_to:
            # `To:` header forged, e.g. for posting on mail.channels, to avoid confusion
            del message['X-Forge-To']
            del message['To']           # avoid multiple To: headers!
            message['To'] = x_forge_to

        # Do not actually send emails in testing mode!
        if getattr(threading.currentThread(), 'testing', False) or self.env.registry.in_test_mode():
            _test_logger.info("skip sending email in test mode")
            return message['Message-Id']

        try:
            message_id = message['Message-Id']
            smtp = smtp_session
            smtp = smtp or self.connect(
                smtp_server, smtp_port, smtp_user, smtp_password,
                smtp_encryption, smtp_debug, mail_server_id=mail_server_id)
            smtp.sendmail(smtp_from, smtp_to_list, message.as_string())
            # do not quit() a pre-established smtp_session
            if not smtp_session:
                smtp.quit()
        except smtplib.SMTPServerDisconnected:
            raise
        except Exception as e:
            params = (ustr(smtp_server), e.__class__.__name__, ustr(e))
            msg = _("Mail delivery failed via SMTP server '%s'.\n%s: %s") % params
            _logger.info(msg)
            raise MailDeliveryException(_("Mail Delivery Failed"), msg)
        return message_id