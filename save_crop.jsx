#target photoshop

// Function to generate a filename with an incrementing number
function generateFilename(outputFolder, baseName, extension) {
    var i = 1;
    var filename;
    do {
        filename = new File(outputFolder + '/' + baseName + '_' + ('000' + i).slice(-3) + extension);
        i++;
    } while (filename.exists);
    return filename;
}

// Ensure there is an active document
if (app.documents.length > 0) {
    var doc = app.activeDocument;

    // Copy the current selection to the clipboard
    doc.selection.copy();

    // Get the clipboard size
    var clipboardWidth = app.activeDocument.width;
    var clipboardHeight = app.activeDocument.height;
    var resolution = app.activeDocument.resolution;

    // Create a new document from the clipboard content
    var newDoc = app.documents.add(clipboardWidth, clipboardHeight, resolution, "New Document from Clipboard", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);
    newDoc.paste();

    // Trim the document to the actual size of the clipboard content
    newDoc.trim(TrimType.TRANSPARENT, true, true, true, true);

    // Generate the filename with incrementing number
    var outputFolder = "path"; // Change this to your desired folder
    var saveFile = generateFilename(outputFolder, "crop", ".png");

    // Save the new document as a PNG file
    var pngSaveOptions = new PNGSaveOptions();
    newDoc.saveAs(saveFile, pngSaveOptions, true, Extension.LOWERCASE);

    // Close the new document without saving changes
    newDoc.close(SaveOptions.DONOTSAVECHANGES);

    // alert("Selection copied and saved to " + saveFile.fsName);
} else {
    alert("No document is open.");
}
