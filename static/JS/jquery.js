// Function to show the description section and hide the review section
function showDescription() {
    document.getElementById("descriptionButton").classList.add("active");
    document.getElementById("reviewButton").classList.remove("active");
    document.getElementById("descriptionSection").style.display = "block";
    document.getElementById("reviewSection").style.display = "none";
  }
  
  // Function to show the review section and hide the description section
  function showReview() {
    document.getElementById("reviewButton").classList.add("active");
    document.getElementById("descriptionButton").classList.remove("active");
    document.getElementById("descriptionSection").style.display = "none";
    document.getElementById("reviewSection").style.display = "block";
  }
  
  // Show the review section by default
  showReview();
  
  document.addEventListener("DOMContentLoaded", function() {
    function scrollToBestSeller(event) {
        event.preventDefault(); // Prevent default anchor behavior
        // Scroll to the element with id="bestseller"
        var bestSellerElement = document.getElementById("bestseller");
        if (bestSellerElement) {
            bestSellerElement.scrollIntoView({ behavior: "smooth" }); // Smooth scrolling
        }
    }

    // Attach event listener to the "BEST SELLER" link
    var bestSellerLink = document.querySelector(".navbar ul li:nth-child(3) a");
    if (bestSellerLink) {
        bestSellerLink.addEventListener("click", scrollToBestSeller);
    }

    // Reattach event listener after page reload
    window.addEventListener("load", function() {
        var bestSellerLink = document.querySelector(".navbar ul li:nth-child(3) a");
        if (bestSellerLink) {
            bestSellerLink.addEventListener("click", scrollToBestSeller);
        }
    });
});
  



