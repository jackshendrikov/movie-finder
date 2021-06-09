document.querySelector(".my-filter").addEventListener("click", function () {
    document.querySelector(".filter-menu").classList.toggle("active");
});

document.querySelector(".grid").addEventListener("click", function () {
    document.querySelector(".list").classList.remove("active");
    document.querySelector(".grid").classList.add("active");
    document.querySelector(".movies-wrapper").classList.add("gridView");
    document.querySelector(".movies-wrapper").classList.remove("tableView");
});

document.querySelector(".list").addEventListener("click", function () {
    document.querySelector(".grid").classList.remove("active");
    document.querySelector(".list").classList.add("active");
    document.querySelector(".movies-wrapper").classList.remove("gridView");
    document.querySelector(".movies-wrapper").classList.add("tableView");
});