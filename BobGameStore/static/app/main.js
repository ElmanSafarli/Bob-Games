let currentSlide = 0;
const slider = document.getElementById('slider');
const dotsContainer = document.getElementById('dots-container');
const images = ['../media/home_page_images/header1.png', '../media/home_page_images/header2.png', '../media/home_page_images/header3.jpg', '../media/home_page_images/header4.jpg'];
const totalSlides = images.length;

document.addEventListener('DOMContentLoaded', function () {
    var swiper = new Swiper('.swiper-container', {
        direction: 'horizontal',
        slidesPerView: 'auto',
        spaceBetween: 10,
        freeMode: true,
        scrollbar: {
            el: '.swiper-scrollbar',
            hide: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.querySelector('#theme-toggle');
    const contacttBlock = document.querySelector('.contact-icon');
    const homeSliderBtnBlock = document.querySelector('.dot.active');
    const trendingTitle = document.querySelector('.trending-title');
    const contactTitle = document.querySelector('.contact-title');
    const contactItemA = document.querySelector('.contact-value a');
    const contactItem = document.querySelector('.contact-value');

    themeToggle.addEventListener('change', function () {
        document.documentElement.classList.toggle('dark-mode', themeToggle.checked);
        contacttBlock.classList.toggle('dark-mode', themeToggle.checked);
        homeSliderBtnBlock.classList.toggle('dark-mode', themeToggle.checked);
        trendingTitle.classList.toggle('dark-mode', themeToggle.checked);
        contactTitle.classList.toggle('dark-mode', themeToggle.checked);
        contactItemA.classList.toggle('dark-mode', themeToggle.checked);
        contactItem.classList.toggle('dark-mode', themeToggle.checked);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.querySelector('#sidebar-theme-toggle');
    const contacttBlock = document.querySelector('.contact-icon');
    const homeSliderBtnBlock = document.querySelector('.dot.active');
    const trendingTitle = document.querySelector('.trending-title');
    const contactTitle = document.querySelector('.contact-title');
    const contactItemA = document.querySelector('.contact-value a');
    const contactItem = document.querySelector('.contact-value');

    themeToggle.addEventListener('change', function () {
        document.documentElement.classList.toggle('dark-mode', themeToggle.checked);
        contacttBlock.classList.toggle('dark-mode', themeToggle.checked);
        homeSliderBtnBlock.classList.toggle('dark-mode', themeToggle.checked);
        trendingTitle.classList.toggle('dark-mode', themeToggle.checked);
        contactTitle.classList.toggle('dark-mode', themeToggle.checked);
        contactItemA.classList.toggle('dark-mode', themeToggle.checked);
        contactItem.classList.toggle('dark-mode', themeToggle.checked);
    });
});


if (document.querySelector(".drop")) {
    const lists = document.querySelectorAll(".drop");
    dropList(lists);

    function dropList(els) {
        els.forEach((el) => {
            el.addEventListener("click", (e) => {
                const clickedList = e.currentTarget;
                const content = clickedList.nextElementSibling;

                // Close all other dropdowns
                lists.forEach((list) => {
                    if (list !== clickedList) {
                        list.classList.remove("show");
                        list.nextElementSibling.style.maxHeight = null;
                    }
                });

                // Toggle the clicked dropdown
                clickedList.classList.toggle("show");

                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        });
    }
}



function showSlide(index) {
    const backgroundImage = `linear-gradient( rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3) ), url('${images[index]}')`;
    slider.style.background = backgroundImage;
    updateDots(index);
}

function updateDots(index) {
    const dots = Array.from(dotsContainer.children);
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

function createDots() {
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        dot.addEventListener('click', () => showSlide(i));
        dotsContainer.appendChild(dot);
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

// Autoload next slide every 5 seconds (adjust as needed)
setInterval(nextSlide, 5000);

// Show initial slide and create dots
showSlide(currentSlide);
createDots();

function changeImage(imageSrc) {
    document.getElementById('mainImage').src = imageSrc;
}

const detailImgMain = document.querySelector('.detail-img-main');
const detailImgMainImg = document.querySelector('.detail-img-main img');

detailImgMain.addEventListener('mousemove', handleMouseMove);
detailImgMain.addEventListener('mouseleave', handleMouseLeave);

function handleMouseMove(e) {
    const { offsetWidth: width, offsetHeight: height } = detailImgMain;
    const { offsetX: x, offsetY: y } = e;

    const xPercent = (x / width) * 100;
    const yPercent = (y / height) * 100;

    detailImgMainImg.style.transformOrigin = `${xPercent}% ${yPercent}%`;
    detailImgMainImg.style.transform = `translate(-${xPercent}%, -${yPercent}%) scale(2)`;
}

function handleMouseLeave() {
    detailImgMainImg.style.transform = 'translate(0, 0) scale(1)';
}

// JavaScript to handle checkbox state changes and submit the form with a delay for the price section
function handleFilterForm(filterForm, formInputs) {
    let updateTimer;  // Variable to store the timer ID

    formInputs.forEach(input => {
        input.addEventListener('change', () => {
            // Clear the existing timer
            clearTimeout(updateTimer);

            // Set a new timer only for the price section
            updateTimer = setTimeout(() => {
                // Create a new URLSearchParams object
                const params = new URLSearchParams();

                // Iterate over the form inputs to gather selected values
                formInputs.forEach(formInput => {
                    if ((formInput.type === 'checkbox' && formInput.checked) || (formInput.type === 'number' && formInput.value !== '')) {
                        params.append(formInput.name, formInput.value);
                    }
                });

                // Handle minimum and maximum price values
                const minPriceInput = filterForm.querySelector('input[name="min_price"]');
                const maxPriceInput = filterForm.querySelector('input[name="max_price"]');
                const minPrice = minPriceInput.value;
                const maxPrice = maxPriceInput.value;

                // Set default value for minimum price to 0 if only maximum price is entered
                if (maxPrice !== '' && (minPrice === '' || isNaN(minPrice))) {
                    minPriceInput.value = 0;
                    params.set('min_price', 0);
                }

                // Add minimum and maximum price to URLSearchParams if values are valid
                if (minPrice !== '' && !isNaN(minPrice)) {
                    params.append('min_price', minPrice);
                }
                if (maxPrice !== '' && !isNaN(maxPrice)) {
                    params.append('max_price', maxPrice);
                }

                // Get the current URL and update the search parameters
                const currentUrl = new URL(window.location.href);
                currentUrl.search = params.toString();

                // Set the form action to the updated URL
                filterForm.setAttribute('action', currentUrl.toString());

                // Submit the form
                filterForm.submit();
            }, input.name.includes('price') ? 1000 : 0); // Use 0 delay for other sections, adjust the delay time for the price section as needed
        });
    });
}

// Add this function to check if a value exists in the array
function isInArray(value, array) {
    return array.includes(value);
}

// Add this function to check the checkboxes based on values in request.GET
function checkCheckboxes(formInputs) {
    formInputs.forEach(formInput => {
        if (formInput.type === 'checkbox' && isInArray(formInput.value, window.location.search)) {
            formInput.checked = true;
        }
    });
}

// Get the product filter form and inputs
const filterForm = document.getElementById('product-filter-form');
const formInputs = filterForm.querySelectorAll('input[type="checkbox"], input[type="number"]');

// Call functions to handle checkbox changes and check checkboxes on page load
handleFilterForm(filterForm, formInputs);
checkCheckboxes(formInputs);

// Get the mobile filter form and inputs
const mobileFilterForm = document.getElementById('mobile-filter-form');
const mobileFormInputs = mobileFilterForm.querySelectorAll('input[type="checkbox"], input[type="number"]');

// Call functions to handle checkbox changes and check checkboxes on page load for mobile form
handleFilterForm(mobileFilterForm, mobileFormInputs);
checkCheckboxes(mobileFormInputs);


