/**
 * 
 */

$(document).ready(function () {
    // Code adapted from http://djangosnippets.org/snippets/1389/  
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.transaction').remove();
            var forms = $('.transaction'); // Get all the forms  
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            var i = 0;
            // Go through the forms and set their indices, names and IDs
            for (formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).children().children().each(function () {
                    if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            alert("You have to enter at least one transaction!");
        }
        return false;
    }

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        // You can only submit a maximum of 10 todo items 
        if (formCount < 10) {
            // Clone a form (without event handlers) from the first form
            var row = $(".transaction:first").clone(false).get(0);
            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".transaction:last").slideDown(300);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");

            // Relabel or rename all the relevant bits
            $(row).children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
            });

            // Add an event handler for the delete item/form link 
            $(row).find(".delete").click(function () {
                return deleteForm(this, prefix);
            });
            
            $(row).find(".trade-date").change(function () {
                return updateValueDate(this)
            });

            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        } // End if
        else {
            alert("Sorry, you can only enter a maximum of ten transactions.");
        }
        return false;
    }
    
    function updateValueDate(tradedate_input) {
    	
    	var trade_date = $(tradedate_input).val();

        var value_date = moment(trade_date).add(2,'days').format('YYYY-MM-DD');

    	var valuedate_tag_id = $(tradedate_input).attr('id');
    	
    	valuedate_tag_id = '#' + valuedate_tag_id.replace("tradedate_d","valuedate_d");

    	$(valuedate_tag_id).val(value_date);

    	return false;
    }
    
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "form");
    });

    $(".delete").click(function () {
        return deleteForm(this, "form");
    });
    
    $(".trade-date").change(function () {
    	return updateValueDate(this)
    });
        
});