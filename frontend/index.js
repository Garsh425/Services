(() => {
    const surname = document.querySelector("#surname");
    const name = document.querySelector("#name");
    const middlename = document.querySelector("#middlename");
    const phone = document.querySelector("#phone");
    const message = document.querySelector("#message");

    function clearForm() {
        surname.value = '';
        name.value = '';
        middlename.value = '';
        phone.value = '';
        message.value = '';
    }

    async function postTicket(data) {
        try {
            const response = await fetch("http://localhost:9090/POST", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error("Сетевая ошибка");
            }
            const responseData = await response.json();
            alert("Обращение отправлено!");
        } catch (err) {
            alert("Ошибка при отправке обращения. Повторите позже.");
            console.error(err);
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('contactForm');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                surname: surname.value,
                name: name.value,
                middlename: middlename.value,
                phone: phone.value,
                message: message.value
            };

            await postTicket(data);
            clearForm();
        });
    });
})();