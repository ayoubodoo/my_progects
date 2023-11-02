# © 2004-2009 Tiny SPRL (<http://tiny.be>).
# © 2015 Agile Business Group <http://www.agilebg.com>
# © 2016 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import os
from datetime import datetime, timedelta
from glob import iglob

from google.api_core import exceptions as GC_exceptions
from google.cloud import storage
from odoo import _, api, exceptions, fields, models
from odoo.service import db

_logger = logging.getLogger(__name__)
try:
    import pysftp
except ImportError:  # pragma: no cover
    _logger.debug('Cannot import pysftp')


class DbBackup(models.Model):
    _inherit = 'db.backup'

    method = fields.Selection(
        [("local", "Local disk"),
         ("sftp", "Remote SFTP server"),
         ("gcloud", "Google cloud storage")],
        default="local",
        help="Choose the storage method for this backup.",
    )
    GOOGLE_APPLICATION_CREDENTIALS = fields.Char("GOOGLE APPLICATION CREDENTIALS PATH")
    bucket_name = fields.Char(string="Bucket ID",
                              help="https://console.cloud.google.com/storage/browser"
                                   "/[bucket-id]/")

    def sftp_connection(self):
        """Return a new SFTP connection with found parameters."""
        self.ensure_one()
        if self.method != 'gcloud':

            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            params = {
                "host": self.sftp_host,
                "username": self.sftp_user,
                "port": self.sftp_port,
                "cnopts": cnopts,
            }
            _logger.debug(
                "Trying to connect to sftp://%(username)s@%(host)s:%(port)d",
                extra=params)
            if self.sftp_private_key:
                params["private_key"] = self.sftp_private_key
                if self.sftp_password:
                    params["private_key_pass"] = self.sftp_password
            else:
                params["password"] = self.sftp_password

            return pysftp.Connection(**params)
        else:
            if self.GOOGLE_APPLICATION_CREDENTIALS:
                os.environ[
                    "GOOGLE_APPLICATION_CREDENTIALS"] = \
                    self.GOOGLE_APPLICATION_CREDENTIALS
            else:
                print("Error: GOOGLE_APPLICATION_CREDENTIALS not specified")
            client = storage.Client()
            bucket = client.get_bucket(self.bucket_name)
            return bucket

    def action_backup(self):
        """Run selected backups."""
        backup = None
        filename = self.filename(datetime.now())
        successful = self.browse()

        gcloud = self.filtered(lambda r: r.method == "gcloud")
        if gcloud:
            if backup:
                cached = open(backup)
            else:
                cached = db.dump_db(self.env.cr.dbname, None)

            with cached:
                for rec in gcloud:
                    with rec.backup_log():
                        bucket = rec.sftp_connection()
                        if bucket:
                            # Directory must exist
                            # try:
                            #     bucket.makedirs(rec.folder)
                            # except pysftp.ConnectionException:
                            #     pass

                            # Copy cached backup to remote server
                            path_to = os.path.join(rec.folder, filename)
                            blob = bucket.blob(path_to)
                            blob.upload_from_file(cached)
                        successful |= rec
            successful.cleanup()

        return super(DbBackup, self).action_backup()

    def action_gcloud_test_connection(self):
        """Check if the Gcloud settings are correct."""
        try:
            if self.sftp_connection():
                raise exceptions.Warning(_("Connection Test Succeeded!"))
        except GC_exceptions.NotFound:
            msg = "Error: Sorry, that bucket (%s) does not exist!" % self.bucket_name
            _logger.info("Connection Test Failed!:" + msg, exc_info=True)
            raise exceptions.Warning(_("Connection Test Failed!\n " + msg))

    @api.depends("folder", "method", "sftp_host", "sftp_port", "sftp_user")
    def _compute_name(self):
        """Get the right summary for this job."""
        for rec in self:
            if rec.method == "local":
                rec.name = "%s @ localhost" % rec.folder
            elif rec.method == "sftp":
                rec.name = "sftp://%s@%s:%d%s" % (
                    rec.sftp_user, rec.sftp_host, rec.sftp_port, rec.folder)
            elif rec.method == "gcloud":
                rec.name = "Gloud: %s/%s" % (
                    rec.bucket_name, rec.folder)

    def cleanup(self):
        """Clean up old backups."""
        now = datetime.now()
        for rec in self.filtered("days_to_keep"):
            with rec.cleanup_log():
                oldest = self.filename(now - timedelta(days=rec.days_to_keep))
                if rec.method == "local":
                    for name in iglob(os.path.join(rec.folder,
                                                   "*.dump.zip")):
                        if os.path.basename(name) < oldest:
                            os.unlink(name)

                elif rec.method == "sftp":
                    with rec.sftp_connection() as remote:
                        for name in remote.listdir(rec.folder):
                            if (name.endswith(".dump.zip") and
                                os.path.basename(name) < oldest):
                                    remote.unlink('%s/%s' % (rec.folder, name))

                elif rec.method == "gcloud":
                    bucket = rec.sftp_connection()
                    if bucket:
                        blobs = bucket.list_blobs(prefix=rec.folder, delimiter=None)
                        for blob in blobs:
                            if blob.name and os.path.basename(blob.name) < oldest:
                                blob.delete()
