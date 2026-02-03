document.addEventListener("DOMContentLoaded", function () {
  const albumInline = document.querySelector("[data-inline-panel='album_images']");

  if (!albumInline) return;

  const uploadButton = document.createElement("button");
  uploadButton.textContent = "📸 Upload Multiple Images";
  uploadButton.type = "button";
  uploadButton.className = "button button-small button-secondary";

  uploadButton.addEventListener("click", async () => {
    const input = document.createElement("input");
    input.type = "file";
    input.multiple = true;
    input.accept = "image/*";

    input.onchange = async (e) => {
      const files = Array.from(e.target.files);
      const addButton = albumInline.querySelector("[data-action-add]");
      if (!addButton) return;

      for (const file of files) {
        addButton.click();
        const lastItem = albumInline.querySelector(".sequence-member:last-child");
        const fileInput = lastItem.querySelector("input[type='file']");
        if (fileInput) {
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          fileInput.files = dataTransfer.files;
        }
      }
    };

    input.click();
  });

  albumInline.parentNode.insertBefore(uploadButton, albumInline);
});
