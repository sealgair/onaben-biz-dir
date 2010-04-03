
$(function() {
    $(".extend-formset").click(function() {
        var formset = $(this).parent(".subformset")
		var last_form = formset.find(".subform").last()
        last_form.clone(true).appendTo(last_form)
		
		var total_input = formset.find("input[name$=TOTAL_FORMS]")
		total_input.val(parseInt(total_input.val())+1)
    })
})

$(function() {
	$(".drop-form").click(function() {
		$(this).parent(".subform").remove()
        var total_input = formset.find("input[name$=TOTAL_FORMS]")
        
		total_input.val(parseInt(total_input.val())-1)
	})
})