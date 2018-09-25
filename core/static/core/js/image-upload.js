$(document).on("click", "i.del" , function() {
	$(this).parent().remove();
});
$(function() {
    $(document).on("change",".upload-file", function()
    {
    		var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test( files[0].type)){ // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function(){ // set image data as src attr of img
            uploadFile.closest(".img-up").find('.img-preview').attr('src', this.result);
            }
        }

    });
});