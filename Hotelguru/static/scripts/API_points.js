document.addEventListener("DOMContentLoaded", function () {
    console.log("JS betöltve");

    const form = document.getElementById("loginForm");

    if (!form) {
        console.log("Nincs loginForm!");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("pwd").value;

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Sikeres bejelentkezés!");
            } else {
                alert(data.message || "Hiba történt!");
            }

        } catch (error) {
            console.error(error);
            alert("Szerver hiba!");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const name = document.getElementById("reg_name").value;
            const email = document.getElementById("reg_email").value;
            const password = document.getElementById("reg_password").value;
            const phone = document.getElementById("reg_phone").value;

            try {
                const response = await fetch("/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password,
                        phone: phone
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Sikeres regisztráció!");

                    const modal = bootstrap.Modal.getInstance(document.getElementById('Register'));
                    modal.hide();

                } else {
                    alert(data.message || "Hiba történt!");
                }

            } catch (error) {
                console.error(error);
                alert("Szerver hiba!");
            }
        });
    }
});

function capitalizeFirst(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
}


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchBtn").addEventListener("click", async function () {
        const city = capitalizeFirst(document.getElementById("citySearch").value);

        if (!city) {
            alert("Adj meg egy várost!");
            return;
        }

        try {
            const response = await fetch(`/listhotels/${city}`);
            const data = await response.json();

            const container = document.getElementById("hotelResults");
            container.innerHTML = "";

            if (!response.ok) {
                container.innerHTML = "<p>Hiba történt</p>";
                return;
            }

            if (data.length === 0) {
                container.innerHTML = "<p>Nincs találat</p>";
                return;
            }

            data.forEach(hotel => {
                const card = `
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${hotel.name}</h5>
                            <p class="card-text">
                                Város: ${hotel.city}<br>
                                Cím: ${hotel.address}<br>
                                Értékelés: ${hotel.rating ?? "N/A"}
                            </p>
                        </div>
                    </div>
                </div>
            `;
                container.innerHTML += card;
            });

        } catch (err) {
            console.error(err);
            alert("Szerver hiba");
        }
    });
});