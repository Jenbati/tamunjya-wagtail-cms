const countdownEl = document.getElementById("countdown");

if (countdownEl && countdownEl.dataset.eventTimestamp) {
  const eventDate =
    parseInt(countdownEl.dataset.eventTimestamp, 10) * 1000; // seconds → ms

  const timer = setInterval(() => {
    const now = Date.now();
    const distance = eventDate - now;

    if (distance <= 0) {
      countdownEl.innerHTML = "कार्यक्रम सम्पन्न भइसकेको छ।";
      clearInterval(timer);
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor(
      (distance % (1000 * 60 * 60)) / (1000 * 60)
    );
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    countdownEl.innerHTML =
      `${days} दिन  ${hours} घण्टा  ${minutes} मिनेट  ${seconds} सेकेन्ड`;
  }, 1000);
}

//   <!-- Script to change modal image -->
document.querySelectorAll(".gallery-img").forEach((img) => {
  img.addEventListener("click", function () {
    document.getElementById("lightboxImage").src = this.getAttribute("data-bs-img");
  });
});

// Gallery for Gallery LightBox

const lightboxModal = document.getElementById("lightboxModal");
const lightboxImage = document.getElementById("lightboxImage");

document.querySelectorAll(".gallery-img").forEach((img) => {
  img.addEventListener("click", () => {
    lightboxImage.src = img.getAttribute("data-bs-img");
  });
});
