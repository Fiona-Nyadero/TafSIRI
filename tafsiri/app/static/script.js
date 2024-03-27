function performSearch() {
    var searchQuery = document.getElementById('searchInput').value;
    var categoryFilter = document.getElementById('categoryFilter').value;
    var countyFilter = document.getElementById('countyFilter').value;

    // Send the search query and filters to the Flask backend
    $.ajax({
        type: 'POST',
        url: '/search',
        data: {
            searchInput: searchQuery,
            categoryFilter: categoryFilter,
            countyFilter: countyFilter
        },
        success: function (results) {
            // Display the filtered results on the page (replace with your actual display logic)
            displayResults(results);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

function displayResults(results) {
    var resultsContainer = $('#searchResults');
    resultsContainer.empty();

    if (results.length > 0) {
        results.forEach(function (result) {
            // Append result data to the results container (customize as needed)
            resultsContainer.append('<div><strong>' + result.name + '</strong>: ' + result.description + '</div>');
        });
    } else {
        resultsContainer.append('<p>No results found.</p>');
    }
}

const images = document.querySelectorAll('.home2_slideshow img');
let currentImageIndex = 0;

function showImage(index) {
    images.forEach((image, i) => {
        if (i === index) {
            image.style.display = 'block';
        } else {
            image.style.display = 'none';
        }
    });
}

function rotateImages() {
    showImage(currentImageIndex);
    currentImageIndex = (currentImageIndex + 1) % images.length;
}

setInterval(rotateImages, 5000); // Rotate every 5 seconds
