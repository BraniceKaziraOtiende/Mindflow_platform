// Wait until the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Back to Top Button
    const backToTopBtn = document.createElement("button");
    backToTopBtn.textContent = "Back to Top";
    backToTopBtn.style.position = "fixed";
    backToTopBtn.style.bottom = "20px";
    backToTopBtn.style.right = "20px";
    backToTopBtn.style.padding = "10px 15px";
    backToTopBtn.style.display = "none"; // Hide initially
    document.body.appendChild(backToTopBtn);

    // Show the back-to-top button when scrolling down
    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = "block";
        } else {
            backToTopBtn.style.display = "none";
        }
    });

    // Scroll back to the top of the page when the button is clicked
    backToTopBtn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Toggle Quick Tips Section
    const quickTipsSection = document.querySelector(".quick-tips");
    const toggleTipsBtn = document.createElement("button");
    toggleTipsBtn.textContent = "Show/Hide Quick Tips";
    toggleTipsBtn.style.display = "block";
    toggleTipsBtn.style.margin = "20px auto";
    toggleTipsBtn.style.padding = "10px";
    quickTipsSection.before(toggleTipsBtn);

    // Show or hide the Quick Tips section when the button is clicked
    toggleTipsBtn.addEventListener("click", () => {
        if (quickTipsSection.style.display === "none") {
            quickTipsSection.style.display = "block";
        } else {
            quickTipsSection.style.display = "none";
        }
    });

    // Interactive Filtering for Articles and Videos (for future extension)
    const articles = document.querySelectorAll(".article");
    const videos = document.querySelectorAll(".video");

    // Example filter function to highlight articles related to "stress"
    function highlightArticles(keyword) {
        articles.forEach(article => {
            const title = article.querySelector("h3").textContent;
            if (title.toLowerCase().includes(keyword.toLowerCase())) {
                article.style.backgroundColor = "#FFEFD5"; // Highlight color
            } else {
                article.style.backgroundColor = "#fff";
            }
        });
    }

    // Example usage: highlight articles with "stress" in the title
    highlightArticles("stress");

    // Future extension: add a search bar to filter content
});
