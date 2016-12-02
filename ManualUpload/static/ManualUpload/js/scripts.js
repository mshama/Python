/**
 * 
 */


//ajaxFormPost = function() {
//    $('#uploadForm').submit( function(e) {
//            // Prevent form submission
//            e.preventDefault();
//            
//           console.log($("#uploadForm").serialize());
//            
//            $.ajax({
//                // You can change the url option to desired target
//                url: "/ManualUpload/uploadData/",
//                csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
//                type: 'post',
////                dataType: 'json',
//                data: $("#uploadForm").serialize(),
//                success: function(responseText, statusText, xhr, $form) {
//                    // Process the response returned by the server ...
//                     console.log(responseText);
//                }
//            });
//        });
//}