      // Countdown Timer
      const eventDate = new Date("2025-10-04T11:00:00").getTime();
      const timer = setInterval(() => {
        let now = new Date().getTime();
        let distance = eventDate - now;

        if (distance < 0) {
          document.getElementById("countdown").innerHTML = "कार्यक्रम समाप्त भइसकेको छ!🎉";
          clearInterval(timer);
          return;
        }

        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor(
          (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById(
          "countdown"
        ).innerHTML = `${days} दिन  ${hours} घण्टा  ${minutes} मिनेट  ${seconds} सेकेन्ड`;
      }, 1000);

    //   <!-- Script to change modal image -->
      document.querySelectorAll(".gallery-img").forEach((img) => {
        img.addEventListener("click", function () {
          document.getElementById("lightboxImage").src =
            this.getAttribute("data-bs-img");
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


