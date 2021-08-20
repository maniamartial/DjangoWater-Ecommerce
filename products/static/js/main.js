 
 //Navbar changing the dropdown menu

 const changeoption = document.getElementById("myselect");
        changeoption.addEventListener('click', changepage);


        function changepage(e) {
            e.preventDefault();
            switch (e.target.value) {

                case 'logout':
                    console.log("Mania")
                   window.open("users/logout","_self")
                    break;

                case 'login':
                  window.open("users/login", "_self")
                    break;

                case 'register':
                   window.open("uses/register", "_self")
                    break;
                case 'account':
                    window.open("users/profile", "_self")
                    break;
            }
        }

        //Display and hide menu bar when changing teh device width
        var hidden_menu = document.getElementById("hidden-menu");
        var button = document.getElementById("display-menu-button");
        var show = document.getElementById("list-menu")
        button.addEventListener('click', function () {
            if (show.style.display === "none") {
                console.log("Tulia")
                show.style.display = "flex"
            }
            else {
                if (hidden_menu.style.display === "none") {
                    show.style.display = "flex";
                }
                else {
                    show.style.display = "none"
                }
            }


        })