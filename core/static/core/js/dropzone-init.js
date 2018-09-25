Dropzone.options.logUpload = {
    paramName: 'log_file',
    maxFilesize: 50,
    maxFiles: 20,
    parallelUploads: 1,
    acceptedFiles: '.txt',

    init: function () {

        var self = this;

        self.on("complete", function(file) {
            self.removeFile(file);
        });

/*        self.on("success", function (file, data) {
            if (data.is_valid == true) {
                alert('Файл ' + file.name + ' успешно загружен');
            }
        });*/

        self.on("queuecomplete", function(data) {
            window.location.reload();
        });
    }
};
