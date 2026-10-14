document.addEventListener("DOMContentLoaded", function () {


    /* =====================================================
       NAVBAR ACTIVE LINK
    ===================================================== */

    const sections = document.querySelectorAll("section[id]");

    const navLinks = document.querySelectorAll(
        ".nav-link"
    );


    window.addEventListener("scroll", function () {

        let current = "";

        sections.forEach(function (section) {

            const sectionTop =
                section.offsetTop - 150;

            const sectionHeight =
                section.offsetHeight;

            if (
                window.scrollY >= sectionTop &&
                window.scrollY < sectionTop + sectionHeight
            ) {

                current = section.getAttribute("id");

            }

        });


        navLinks.forEach(function (link) {

            link.classList.remove("active");

            if (
                link.getAttribute("href") ===
                "#" + current
            ) {

                link.classList.add("active");

            }

        });

    });



    /* =====================================================
       BACK TO TOP
    ===================================================== */

    const backToTop =
        document.getElementById("backToTop");


    window.addEventListener("scroll", function () {

        if (window.scrollY > 500) {

            backToTop.classList.add("show");

        } else {

            backToTop.classList.remove("show");

        }

    });



    /* =====================================================
       PROJECT FILTER
    ===================================================== */

    const filterButtons =
        document.querySelectorAll(".filter-btn");

    const projectItems =
        document.querySelectorAll(".project-item");


    filterButtons.forEach(function (button) {

        button.addEventListener("click", function () {


            filterButtons.forEach(function (btn) {

                btn.classList.remove("active");

            });


            this.classList.add("active");


            const filter =
                this.getAttribute("data-filter");


            projectItems.forEach(function (project) {


                const category =
                    project.getAttribute("data-category");


                if (
                    filter === "all" ||
                    category === filter
                ) {

                    project.style.display = "";

                } else {

                    project.style.display = "none";

                }

            });

        });

    });



    /* =====================================================
       SMOOTH MOBILE NAVIGATION
    ===================================================== */

    const mobileLinks =
        document.querySelectorAll(
            ".navbar-collapse .nav-link"
        );


    const navbarCollapse =
        document.getElementById(
            "mainNavigation"
        );


    mobileLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            if (
                navbarCollapse.classList.contains("show")
            ) {

                const bsCollapse =
                    bootstrap.Collapse.getInstance(
                        navbarCollapse
                    );

                if (bsCollapse) {

                    bsCollapse.hide();

                }

            }

        });

    });



    /* =====================================================
       CONTACT FORM DEMO
    ===================================================== */

    const contactForm =
        document.querySelector(
            ".contact-form-card form"
        );


    if (contactForm) {

        contactForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();

                alert(
                    "Thank you! Your message form is ready to be connected to Django."
                );

            }
        );

    }


});