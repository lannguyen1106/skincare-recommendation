// Script for configuring FilePond, a file upload library.
// See https://github.com/pqina/filepond for more information.

FilePond.setOptions({
    instantUpload: true,
    allowMultiple: false,
    allowReplace: false,
    allowImagePreview: true,
    server: {
      process: '/upload',
      fetch: null,
      revert: null,
      restore: null,
      load: null
    }
  });
  FilePond.registerPlugin(
    FilePondPluginImagePreview
  );
  const pond = FilePond.create(document.querySelector('input[type="file"]'));
  pond.on('processfile', (error, file) => {
    if (error === null) {
      let id = file.serverId;
      let uploadFileIdInputNode = document.querySelector(`#image`);
      uploadFileIdInputNode.value = id;
    }
  })