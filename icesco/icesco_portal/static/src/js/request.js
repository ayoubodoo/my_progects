function fixIds(elem, cntr) {
    $(elem).find("[id]").add(elem).each(function () {
        this.id = this.id + '_' + cntr;
        this.name = this.name + '_' + cntr;

    })
};

odoo.define('icesco_portal.create_req', function (require) {
    'use strict';
    //    require('web.dom_ready');
    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var time = require('web.time');
    var qweb = core.qweb;
    var _t = core._t;
    console.log('==== op ======')
    console.log("==========>1")

    $("#goal_id").change(function () {
            var x = document.getElementById("goal_id").value;
            let goals = rpc.query({
              model: 'dh.pilliar',
              method: 'pillars_possible_search_read',
              kwargs: {
                'goal': parseInt(x),
                'fields': ['id', 'name', 'name_name'],
                'offset': 0,
                'limit': 100
              },
              //context: {},
            });
            var select = document.getElementById("pillar_id")


            goals.then(rules => {
            if (rules) {
                select.length = 1;
                for(var i = 0; i < rules.length; i++) {
                    var option = document.createElement("OPTION"),
                        txt = document.createTextNode(rules[i]['name_name'])
                        option.appendChild(txt);
                        option.setAttribute("value", rules[i]['id']);
                        select.insertBefore(option, select.lastChild);
                }
                if (rules.length == 0){
                    select.length = 1;
                }
                console.log('rules', rules)
                }
            else {

                   }
        });
    });

    $("#pillar_id").change(function () {
            var x = document.getElementById("pillar_id").value;
            let pilars = rpc.query({
              model: 'project.project',
              method: 'projects_possible_search_read',
              kwargs: {
                'pillar': parseInt(x),
                'fields': ['id', 'name'],
                'offset': 0,
                'limit': 100
              },
              //context: {},
            });
            var select = document.getElementById("project_id")


            pilars.then(rules => {
            if (rules) {
                select.length = 1;
                for(var i = 0; i < rules.length; i++) {
                    var option = document.createElement("OPTION"),
                        txt = document.createTextNode(rules[i]['name'])
                        option.appendChild(txt);
                        option.setAttribute("value", rules[i]['id']);
                        select.insertBefore(option, select.lastChild);
                }
                if (rules.length == 0){
                    select.length = 1;
                }
                }
            else {

                   }
        });
    });



    $("#project").change(function () {
            var x = document.getElementById("project").value;
           let projects = rpc.query({
              model: 'project.task',
              method: 'tasks_possible_search_read',
              kwargs: {
                'project': parseInt(x),
                'fields': ['id', 'name'],
                'offset': 0,
                'limit': 100
              },
              //context: {},
            });
            var select = document.getElementById("task")


            projects.then(rules => {
            if (rules) {
                select.length = 1;
                for(var i = 0; i < rules.length; i++) {
                    var option = document.createElement("OPTION"),
                        txt = document.createTextNode(rules[i]['name'])
                        option.appendChild(txt);
                        option.setAttribute("value", rules[i]['id']);
                        select.insertBefore(option, select.lastChild);
                }
                if (rules.length == 0){
                    select.length = 1;
                }
                }
            else {

                   }
        });
    });

//     var myEle = document.getElementById("official_language");
//         if(myEle){
//             let partner = rpc.query({
//               model: 'res.partner',
//               method: 'my_search_read_official_language',
//               kwargs: {
//                 'domain': [],
//                 'fields': [],
//                 'offset': 0,
//                 'limit': 100
//               },
//               //context: {},
//             });
//             console.log(partner);
//             partner.then(rules => {
//             if (rules[0] !== undefined) {
//                 for (let l = 1; l < rules.length; l++) {
//
//                     console.log("==========>2022", rules[l]['key'])
//                     $('#addr_official_language').show();
//                     var test = $('#addr_official_language div:last').clone();
//                     var tab_len = $('#addr_official_language div').length;
//                     fixIds(test, l);
//                     test.attr("id", "official_language_" + (l));
// //                     test.attr("name", "official_language_" + (l));
//                     test.find('select').each(function() {
//                         this.name= "official_language_" + (l);
//                     });
// //                     var c_id = "_" + (tab_len)
//
//                     $('#addr_official_language div:last').after(test);
//                     $("#official_language_" + l).val('');
// //                     document.getElementsByName("official_language_" + l).value=rules[l]['key'];
//                     var mySelect = document.getElementsByName("official_language_" + l);
//
// //                     $mySelect.selectedIndex = rules[l]['key']
//                     for(var i, j = 0; i = mySelect[0].options[j]; j++) {
//                         if (rules[l]['key'] != false){
//                             if(i.value == rules[l]['key'].toString()) {
//                                 mySelect[0].selectedIndex = j;
//                                 break;
//                             }
//                         }
//                     }
//                 }
//
//
//            }
//
//             });
//     }

//     var myEle_days = document.getElementById("tab_other_enational_days");
//         if(myEle_days){
//             let partner = rpc.query({
//               model: 'res.partner',
//               method: 'my_search_read_national_days',
//               kwargs: {
//                 'domain': [],
//                 'fields': [],
//                 'offset': 0,
//                 'limit': 100
//               },
//               //context: {},
//             });
//             console.log(partner);
//                 partner.then(rules => {
//                 if (rules[0] !== undefined) {
//                     for (let l = 1; l < rules.length; l++) {
//
//                         var tab_len = $('#tab_other_national_days tbody tr').length;
//                         var correct_id = ""
//                         if (tab_len >= 2) {
//                             correct_id = "_" + l
//                         }
//                         var hex = $("#name_national_days" + correct_id).val();
//                         var rgb = $("#national_days" + correct_id).val();
//
//                         console.log("==========>2")
//                         $('#addr_national_days').show();
//                         var test = $('#addr_national_days').clone();
//                         var tab_len = $('#tab_other_national_days tbody tr').length;
//                         fixIds(test, l);
//                         test.attr("id", "addr_national_days_" + l);
//                         test.attr("name", "addr_national_days_" + l);
//
//                         $('#tab_other_national_days tr:last').after(test);
//                         if (rules[l]['name'] != false){
//                             $("#name_national_days_" + l).val(rules[l]['name']);
//                         }
//                         else{
//                             $("#name_national_days_" + l).val('');
//                         }
//                        if (rules[l]['date'] != false){
//                             $("#name_national_days_" + l).val(rules[l]['date']);
//                         }
//                         else{
//                             $("#name_national_days_" + l).val('');
//                         }
//
//                     }
//
//
//            }
//
//             });
//     }

//     var myEle_flag_color = document.getElementById("tab_logic_flag_color");
//     if(myEle_flag_color){
//         let partner = rpc.query({
//           model: 'res.partner',
//           method: 'my_search_read_flag_color',
//           kwargs: {
//             'domain': [],
//             'fields': [],
//             'offset': 0,
//             'limit': 100
//           },
//           //context: {},
//         });
//         console.log(partner);
//         partner.then(rules => {
//         if (rules[0] !== undefined) {
//             for (let l = 1; l < rules.length; l++) {
//
//                 var tab_len = $('#tab_logic_flag_color tbody tr').length;
//                 var correct_id = ""
//                 if (tab_len >= 2) {
//                     correct_id = "_" + l
//                 }
//                 var hex = $("#hex" + correct_id).val();
//                 var rgb = $("#rgb" + correct_id).val();
//
//                 console.log("==========>2")
//                 $('#addr_flag_color').show();
//                 var test = $('#addr_flag_color').clone();
//                 var tab_len = $('#tab_logic_flag_color tbody tr').length;
//                 fixIds(test, l);
//                 test.attr("id", "addr_flag_color_" + l);
//                 test.attr("name", "addr_flag_color_" + l);
//
//                 $('#tab_logic_flag_color tr:last').after(test);
//                 if (rules[l]['hex'] != false){
//                     $("#hex_" + l).val(rules[l]['hex']);
//                 }
//                 else{
//                     $("#hex_" + l).val('');
//                 }
//                 if (rules[l]['rgb'] != false){
//                     $("#rgb_" + l).val(rules[l]['rgb']);
//                 }
//                 else{
//                     $("#rgb_" + l).val('');
//                 }
//
//             }
//
//
//        }
//
//         });
//     }

    var myEle_government_officials = document.getElementById("tab_logic_government_officials");
    if(myEle_government_officials){
        let partner = rpc.query({
          model: 'res.partner',
          method: 'my_search_read_government_officials',
          kwargs: {
            'domain': [],
            'fields': [],
            'offset': 0,
            'limit': 100
          },
          //context: {},
        });
        console.log(partner);
        partner.then(rules => {
        if (rules[0] !== undefined) {
            for (let l = 1; l < rules.length; l++) {

                var tab_len = $('#tab_logic_government_officials tbody tr').length;
                var correct_id = ""
                if (tab_len >= 2) {
                    correct_id = "_" + l
                }
                var hex = $("#title" + correct_id).val();
                var rgb = $("#official_name" + correct_id).val();
                var rgb = $("#position" + correct_id).val();
                var rgb = $("#contact_email" + correct_id).val();
                var rgb = $("#phone" + correct_id).val();
                var rgb = $("#since" + correct_id).val();
                var rgb = $("#website" + correct_id).val();

                console.log("==========>2")
                $('#addr_government_officials').show();
                var test = $('#addr_government_officials').clone();
                var tab_len = $('#tab_logic_government_officials tbody tr').length;
                fixIds(test, l);
                test.attr("id", "addr_government_officials_" + l);
                test.attr("name", "addr_government_officials_" + l);

                $('#tab_logic_government_officials tr:last').after(test);
                if (rules[l]['title'] != false){
                    $("#title_" + l).val(rules[l]['title']);
                }
                else{
                    $("#title_" + l).val('');
                }
                if (rules[l]['official_name'] != false){
                    $("#official_name_" + l).val(rules[l]['official_name']);
                }
                else{
                    $("#official_name_" + l).val('');
                }
                if (rules[l]['position'] != false){
                    $("#position_" + l).val(rules[l]['position']);
                }
                else{
                    $("#position_" + l).val('');
                }
                if (rules[l]['contact_email'] != false){
                    $("#contact_email_" + l).val(rules[l]['contact_email']);
                }
                else{
                    $("#contact_email_" + l).val('');
                }
                if (rules[l]['phone'] != false){
                    $("#phone_" + l).val(rules[l]['phone']);
                }
                else{
                    $("#phone_" + l).val('');
                }
                if (rules[l]['since'] != false){
                    $("#since_" + l).val(rules[l]['since']);
                }
                else{
                    $("#since_" + l).val('');
                }
                if (rules[l]['website'] != false){
                    $("#website_" + l).val(rules[l]['website']);
                }
                else{
                    $("#website_" + l).val('');
                }

            }


       }

        });
    }

    var myEle_commission_teams = document.getElementById("tab_logic_commission_teams");
    if(myEle_commission_teams){
        let partner = rpc.query({
          model: 'res.partner',
          method: 'my_search_read_commission_teams',
          kwargs: {
            'domain': [],
            'fields': [],
            'offset': 0,
            'limit': 100
          },
          //context: {},
        });
        console.log(partner);
        partner.then(rules => {
        if (rules[0] !== undefined) {
            for (let l = 1; l < rules.length; l++) {

                var tab_len = $('#tab_logic_commission_teams tbody tr').length;
                var correct_id = ""
                if (tab_len >= 2) {
                    correct_id = "_" + l
                }
                var hex = $("#title_commission_team" + correct_id).val();
                var rgb = $("#official_name_commission_team" + correct_id).val();
                var rgb = $("#contact_email_commission_team" + correct_id).val();
                var rgb = $("#phone_commission_team" + correct_id).val();

                console.log("==========>2")
                $('#addr_commission_teams').show();
                var test = $('#addr_commission_teams').clone();
                var tab_len = $('#tab_logic_commission_teams tbody tr').length;
                fixIds(test, l);
                test.attr("id", "addr_commission_teams_" + l);
                test.attr("name", "addr_commission_teams_" + l);

                $('#tab_logic_commission_teams tr:last').after(test);
                if (rules[l]['title'] != false){
                    $("#title_commission_team_" + l).val(rules[l]['title']);
                }
                else{
                    $("#title_commission_team_" + l).val('');
                }
                if (rules[l]['official_name'] != false){
                    $("#official_name_commission_team_" + l).val(rules[l]['official_name']);
                }
                else{
                    $("#official_name_commission_team_" + l).val('');
                }
                if (rules[l]['contact_email'] != false){
                    $("#contact_email_commission_team_" + l).val(rules[l]['contact_email']);
                }
                else{
                    $("#contact_email_commission_team_" + l).val('');
                }
                if (rules[l]['phone'] != false){
                    $("#phone_commission_team_" + l).val(rules[l]['phone']);
                }
                else{
                    $("#phone_commission_team_" + l).val('');
                }

            }


       }

        });
    }

//     $("#vendor").change(function () {
//         console.log("==========>2")
//         var x = document.getElementById("vendor").value;
//         let partner = rpc.query({
//           model: 'res.partner',
//           method: 'my_search_read',
//           kwargs: {
//             'domain': [['id', '=', parseInt(x)]],
//             'fields': ['id', 'name', 'property_purchase_currency_id'],
//             'offset': 0,
//             'limit': 10
//           },
//           //context: {},
//         });
//         console.log(partner);
//         partner.then(rules => {
//         if (rules[0] !== undefined) {
//            document.getElementById("devise").innerHTML = rules[0]['property_purchase_currency_id'][1]
//
//        } else {
//            document.getElementById("devise").innerHTML = ''
//             console.log(rules[0])
//        }
//
//         });
//     })


    var i = 1;
    var see = $('#addr_official_language').attr("see");
    $("#add_row_official_language").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#addr_official_language official_language').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }

        console.log($('#addr_official_language div').length)

        if ($('#addr_official_language div').length == 1 && see) {
            $('#addr_official_language div').show()
            see = false
        } else {
            console.log("==========>2022")
            $('#addr_official_language').show();
            var test = $('#addr_official_language div:last').clone();
            var tab_len = $('#addr_official_language div').length;
            fixIds(test, tab_len);
            test.attr("id", "official_language_" + (tab_len));
            test.attr("name", "official_language_" + (tab_len));
            test.find('select').each(function() {
                this.name= "official_language_" + (tab_len);
            });
            var c_id = "_" + (tab_len)

            $('#addr_official_language div:last').after(test);
            $("#official_language" + c_id).val('');

            }

        var $count = $("#cart-item-count");
        var $rowCount = $('#official_language:last').index() + 1;
        var a = $rowCount;
        $("#delete_row_official_language").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row_official_language").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row_official_language").click(function () {
        i--;
        if ($('#addr_official_language div').length == 1) {
            $('#addr_official_language div').hide()
            see = true
//             alert("Vous ne pouvez pas supprimer la première ligne.")
            console.log("==========>4")

        } else {
            console.log("==========>5")
            $('#addr_official_language div:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('#addr_official_language div:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row_used_language").prop("disabled", true);
        }

    });


    var i = 1;
    var see = $('#addr_used_language').attr("see");
    $("#add_row_used_language").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#addr_used_language used_language').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }

        console.log($('#addr_used_language div').length)

        if ($('#addr_used_language div').length == 1 && see) {
            $('#addr_used_language div').show()
            see = false
        } else {
            console.log("==========>2022")
            $('#addr_used_language').show();
            var test = $('#addr_used_language div:last').clone();
            var tab_len = $('#addr_used_language div').length;
            fixIds(test, tab_len);
            test.attr("id", "used_language_" + (tab_len));
            test.attr("name", "used_language_" + (tab_len));
            test.find('select').each(function() {
                this.name= "used_language_" + (tab_len);
            });
            var c_id = "_" + (tab_len)

            $('#addr_used_language div:last').after(test);
            $("#used_language" + c_id).val('');

            }

        var $count = $("#cart-item-count");
        var $rowCount = $('#used_language:last').index() + 1;
        var a = $rowCount;
        $("#delete_row_used_language").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row_used_language").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row_used_language").click(function () {
        i--;
        if ($('#addr_used_language div').length == 1) {
            $('#addr_used_language div').hide()
            see = true
//             alert("Vous ne pouvez pas supprimer la première ligne.")
            console.log("==========>4")

        } else {
            console.log("==========>5")
            $('#addr_used_language div:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('#addr_used_language div:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row_official_language").prop("disabled", true);
        }

    });


    var see = $('#addr_national_days').attr("see");
    $("#add_row_national_days").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#tab_other_national_days tbody tr').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }
        var hex = $("#name_national_days" + correct_id).val();
        var rgb = $("#national_days" + correct_id).val();

        if ($('#tab_other_national_days tbody tr').length == 1 && see) {
            $('#addr_national_days').show()
            see = false
        } else {
            console.log("==========>2")
            $('#addr_national_days').show();
            var test = $('#addr_national_days').clone();
            var tab_len = $('#tab_other_national_days tbody tr').length;
            fixIds(test, tab_len);
            test.attr("id", "addr_national_days_" + (tab_len + 1));
            test.attr("name", "addr_national_days_" + (tab_len + 1));
            var c_id = "_" + (tab_len)

            $('#tab_other_national_days tr:last').after(test);
            $("#name_national_days" + c_id).val('');
            $("#national_days" + c_id).val('');
            }


        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_other_national_days tr:last').index() + 1;
        var a = $rowCount;
        $("#delete_row_national_days").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row_national_days").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row_national_days").click(function () {
        i--;
        console.log("==========>3")
        if ($('#tab_other_national_days tbody tr').length == 1) {
            $('#addr_national_days').hide()
            see = true
//             alert("Vous ne pouvez pas supprimer la première ligne.")

        } else {
            $('#tab_other_national_days tr:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_other_national_days tr:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row_national_days").prop("disabled", true);
        }

    });



//     var i = 1;
//     var see = $('#addr_national_days').attr("see");
//     $("#add_row_national_days").click(function (e) {
//         console.log("==========>1")
//         var tab_len = $('#addr_national_days national_days').length;
//         var correct_id = ""
//         if (tab_len >= 2) {
//             correct_id = "_" + (tab_len - 1)
//         }
//
//         console.log($('#addr_national_days div').length)
//
//         if ($('#addr_national_days div').length == 1 && see) {
//             $('#addr_national_days div').show()
//             see = false
//         } else {
//             console.log("==========>2022")
//             $('#addr_national_days').show();
//             var test = $('#addr_national_days div:last').clone();
//             var tab_len = $('#addr_national_days div').length;
//             fixIds(test, tab_len);
//             test.attr("id", "national_days_" + (tab_len));
//             test.attr("name", "national_days_" + (tab_len));
//             test.find('input').each(function() {
//                 this.name= "national_days_" + (tab_len);
//             });
//             var c_id = "_" + (tab_len)
//
//             $('#addr_national_days div:last').after(test);
//             $("#national_days" + c_id).val('');
//
//             }
//
//         var $count = $("#cart-item-count");
//         var $rowCount = $('#national_days:last').index() + 1;
//         var a = $rowCount;
//         $("#delete_row_national_days").prop("disabled", !a);
//         $count.text(a);
//         ++i;
//     });
//
//     $("#delete_row_national_days").prop("disabled", !$("#cart-item-count").val());
//
//     $("#delete_row_national_days").click(function () {
//         i--;
//         if ($('#addr_national_days div').length == 1) {
//             $('#addr_national_days div').hide()
//             see = true
// //             alert("Vous ne pouvez pas supprimer la première ligne.")
//             console.log("==========>4")
//
//         } else {
//             console.log("==========>5")
//             $('#addr_national_days div:last').remove().end();
//         }
//
//         var $count = $("#cart-item-count");
//         var $rowCount = $('#addr_national_days div:last').index() + 1;
//         var b = $rowCount;
//         if (b >= 1) {
//             $count.text(b);
//         } else {
//             $("#delete_row_national_days").prop("disabled", true);
//         }
//
//     });


    var i = 1;
    var see = $('#addr_flag_color').attr("see");
    $("#add_row_flag_color").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#tab_logic_flag_color tbody tr').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }
        var hex = $("#hex" + correct_id).val();
        var rgb = $("#rgb" + correct_id).val();

        if ($('#tab_logic_flag_color tbody tr').length == 1 && see) {
            $('#addr_flag_color').show()
            see = false
        } else {
            // $('#addr_flag_color').each(function () {
            console.log("==========>2")
            // });
            $('#addr_flag_color').show();
            var test = $('#addr_flag_color').clone();
            var tab_len = $('#tab_logic_flag_color tbody tr').length;
            fixIds(test, tab_len);
            test.attr("id", "addr_flag_color_" + (tab_len + 1));
            test.attr("name", "addr_flag_color_" + (tab_len + 1));
            var c_id = "_" + (tab_len)

            $('#tab_logic_flag_color tr:last').after(test);
//             $("#hex" + c_id).val(hex);
            $("#hex" + c_id).val('');
//             $("#rgb" + c_id).val(rgb);
            $("#rgb" + c_id).val('');

//            $("#line_id" + c_id).val('0');
            }

//             $("#delete_row_line" + c_id).click(function (e) {
//                 var row = this
//                 var tr_node = row.parentNode.parentNode
//                 var tab_len = $('#tab_logic_flag_color tbody tr').length;
//                 if (tab_len == 1) {
//                     $('#addr_flag_color').hide()
//                     alert("Vous ne pouvez pas supprimer la première ligne.")
//                 } else {
//                     if (row.parentNode != null) {
//                         row.parentNode.removeChild(row);
//                         var count = addr_flag_colorr_id
//                         console.log("==========>", count)
//                         for (let i = addr_flag_color_id + 1; i < tab_len + addr_flag_color_id; i++) {
//                             if (count == 0) {
//                                 if ($('#addr_flag_color' + i).length) {
//                                     $('#hex_' + i).prop("name", "hex")
//                                     $('#rgb_' + i).prop("name", "rgb")
//                                 }
//                             } else {
//                                 if ($('#addr_flag_color' + i).length) {
//                                     $('#hex_' + i).prop("name", "hex_" + count)
//                                     $('#rgb_' + i).prop("name", "rgb_" + count)
//                                     count = i - 1
//                                 }
//                             }
//                             console.log(count)
//
//                         }
//                     }
//
//                 }
//
//
//
//             });
//         }

        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic_flag_color tr:last').index() + 1;
        var a = $rowCount;
        $("#delete_row_flag_color").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row_flag_color").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row_flag_color").click(function () {
        i--;
        console.log("==========>3")
        if ($('#tab_logic_flag_color tbody tr').length == 1) {
            $('#addr_flag_color').hide()
            see = true
//             alert("Vous ne pouvez pas supprimer la première ligne.")

        } else {
            $('#tab_logic_flag_color tr:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic_flag_color tr:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row_flag_color").prop("disabled", true);
        }

    });


    var i = 1;
    var see = $('#addr_government_officials').attr("see");
    $("#add_row_government_officials").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#tab_logic_government_officials tbody tr').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }
        var title = $("#title" + correct_id).val();
        var official_name = $("#official_name" + correct_id).val();
        var position = $("#position" + correct_id).val();
        var contact_email = $("#contact_email" + correct_id).val();
        var phone = $("#phone" + correct_id).val();

        if ($('#tab_logic_government_officials tbody tr').length == 1 && see) {
            $('#addr_government_officials').show()
            see = false
        } else {
            console.log("==========>2")
            $('#addr_government_officials').show();
            var test = $('#addr_government_officials').clone();
            var tab_len = $('#tab_logic_government_officials tbody tr').length;
            fixIds(test, tab_len);
            test.attr("id", "addr_government_officials_" + (tab_len + 1));
            test.attr("name", "addr_government_officials_" + (tab_len + 1));
            var c_id = "_" + (tab_len)

            $('#tab_logic_government_officials tr:last').after(test);
            $("#title" + c_id).val('');
            $("#official_name" + c_id).val('');
            $("#position" + c_id).val('');
            $("#contact_email" + c_id).val('');
            $("#phone" + c_id).val('');

            }


        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic_government_officials tr:last').index() + 1;
        var a = $rowCount;
        $("#delete_row_government_officials").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row_government_officials").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row_government_officials").click(function () {
        i--;
        console.log("==========>3")
        if ($('#tab_logic_government_officials tbody tr').length == 1) {
            $('#addr_government_officials').hide()
            see = true
//             alert("Vous ne pouvez pas supprimer la première ligne.")

        } else {
            $('#tab_logic_government_officials tr:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic_government_officials tr:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row_government_officials").prop("disabled", true);
        }

    });


    var i = 1;
    var see = $('#addr_commission_teams').attr("see");
    $("#add_row_commission_teams").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#tab_logic_commission_teams tbody tr').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }
        var title = $("#title_commission_team" + correct_id).val();
        var official_name = $("#official_name_commission_team" + correct_id).val();
        var contact_email = $("#contact_email_commission_team" + correct_id).val();
        var phone = $("#phone_commission_team" + correct_id).val();

        if ($('#tab_logic_commission_teams tbody tr').length == 1 && see) {
            $('#addr_commission_teams').show()
            see = false
        } else {
            console.log("==========>2")
            $('#addr_commission_teams').show();
            var test = $('#addr_commission_teams').clone();
            var tab_len = $('#tab_logic_commission_teams tbody tr').length;
            fixIds(test, tab_len);
            test.attr("id", "addr_commission_teams_" + (tab_len + 1));
            test.attr("name", "addr_commission_teams_" + (tab_len + 1));
            var c_id = "_" + (tab_len)

            $('#tab_logic_commission_teams tr:last').after(test);
            $("#title_commission_team" + c_id).val('');
            $("#official_name_commission_team" + c_id).val('');
            $("#contact_email_commission_team" + c_id).val('');
            $("#phone_commission_team" + c_id).val('');

            }


        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic_commission_teams tr:last').index() + 1;
        var a = $rowCount;
        $("#delete_row_commission_teams").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row_commission_teams").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row_commission_teams").click(function () {
        i--;
        console.log("==========>3")
        if ($('#tab_logic_commission_teams tbody tr').length == 1) {
            $('#addr_commission_teams').hide()
            see = true
//             alert("Vous ne pouvez pas supprimer la première ligne.")

        } else {
            $('#tab_logic_commission_teams tr:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic_commission_teams tr:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row_commission_teams").prop("disabled", true);
        }

    });

//    proposition

    var i = 1;
    var see = $('#addr').attr("see");
    $("#add_row").click(function (e) {
        console.log("==========>1")
        var tab_len = $('#tab_logic tbody tr').length;
        var correct_id = ""
        if (tab_len >= 2) {
            correct_id = "_" + (tab_len - 1)
        }
        var category = $("#invite_name" + correct_id).val();
        var compte_analytic = $("#job_title" + correct_id).val();
        var description = $("#attachment_ids" + correct_id).val();

        if ($('#tab_logic tbody tr').length == 1 && see) {
            $('#addr').show()
            see = false
        } else {
            // $('#addr').each(function () {
            // });
            $('#addr').show();
            var test = $('#addr').clone();
            var tab_len = $('#tab_logic tbody tr').length;
            fixIds(test, tab_len);
            test.attr("id", "addr_" + (tab_len + 1));
            test.attr("name", "addr_" + (tab_len + 1));
            var c_id = "_" + (tab_len)

            $('#tab_logic tr:last').after(test);
            $("#invite_name" + c_id).val(category);
            $("#job_title" + c_id).val(compte_analytic);
            $("#attachment_ids" + c_id).val('');

            $("#delete_row_line" + c_id).click(function (e) {
                var row = this
                var tr_node = row.parentNode.parentNode
                var tab_len = $('#tab_logic tbody tr').length;
                if (tab_len == 1) {
                    $('#addr').hide()
                    alert("Vous ne pouvez pas supprimer la première ligne.")
                } else {
                    if (row.parentNode != null) {
                        row.parentNode.removeChild(row);
                        var count = addr_id
                        console.log("==========>", count)
                        for (let i = addr_id + 1; i < tab_len + addr_id; i++) {
                            if (count == 0) {
                                if ($('#addr' + i).length) {
                                    $('#invite_name_' + i).prop("name", "invite_name")
                                    $('#job_title_' + i).prop("name", "job_title")
                                    $('#attachment_ids_' + i).prop("name", "attachment_ids")
                                }
                            } else {
                                if ($('#addr' + i).length) {
                                    $('#invite_name_' + i).prop("name", "invite_name" + count)
                                    $('#job_title_' + i).prop("name", "job_title" + count)
                                    $('#attachment_ids_' + i).prop("name", "attachment_ids" + count)
                                    count = i - 1
                                }
                            }
                            console.log(count)

                        }
                    }

                }



            });
        }


        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic tr:last').index() + 1;
        var a = $rowCount;
        $("#delete_row").prop("disabled", !a);
        $count.text(a);
        ++i;
    });

    $("#delete_row").prop("disabled", !$("#cart-item-count").val());

    $("#delete_row").click(function () {
        i--;
        console.log("==========>3")
        if ($('#tab_logic tbody tr').length == 1) {
            $('#addr').hide()
            see = true

        } else {
            $('#tab_logic tr:last').remove().end();
        }

        var $count = $("#cart-item-count");
        var $rowCount = $('table#tab_logic tr:last').index() + 1;
        var b = $rowCount;
        if (b >= 1) {
            $count.text(b);
        } else {
            $("#delete_row").prop("disabled", true);
        }

    });

});