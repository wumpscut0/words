let ruGlobalWanish = true;
let enGlobalWanish = true;


class Api {
     BASE_URL = "http://26.234.36.149:8000/api/v1/words";
//    BASE_URL = "http://localhost:8000/api/v1/words";
    
    async removeWordFromFavorite(word_id, user_id) {
        return await fetch(`${this.BASE_URL}/delete?word_id=${word_id}&user_id=${user_id}`, {
            method: "DELETE",
            // headers: {
            //     "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute("content"),
            // },
            // credentials: 'same-origin'
        });
    };

    async addWordToFavorite(word_id, user_id) {
        return await fetch(`${this.BASE_URL}/add?word_id=${word_id}&user_id=${user_id}`, {
            method: "POST",
            // headers: {
            //     "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute("content"),
            // },
            // credentials: 'same-origin'
        });
    };
};

const api = new Api();

document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("words");
    const enCol = document.getElementById("enCol");
    const ruCol = document.getElementById("ruCol");
    const rows = table.querySelectorAll("tr");
    
    rows.forEach(row => {
        row.querySelectorAll("td").forEach((entry, index)=> {
            if (index === 2) {
                const button = entry.querySelector("button")
                button.addEventListener("click", async () => {
                    const [word_id, user_id] = button.value.split(":");
                    if (button.classList.contains("btn-danger")) {
                        api.removeWordFromFavorite(word_id, user_id);
                        button.classList.replace("btn-danger", "btn-primary");
                        button.textContent = "Add";
                    } else {
                        api.addWordToFavorite(word_id, user_id);
                        button.classList.replace("btn-primary", "btn-danger");
                        button.textContent = "Remove";
                    };
                });
            } else {
                entry.addEventListener("click", () => {
                    entry.classList.toggle("white")
//                    if (!entry.style.color) {
//                        entry.style.color = "white"
//					} else {
//                         if (entry.style.color === "black") {
//                             entry.style.color = "white";
//                         } else {
//                             entry.style.color = "black";
//                         };
//                    }
                });
            };
        });
    });
    
    enCol.addEventListener("click", () => {
        rows.forEach(row => {
            entry = row.querySelectorAll("td")[0];
            if (enGlobalWanish) {
                entry.style.color = "black";
            } else {
                entry.style.color = "white";
            };
        });
        enGlobalWanish = !enGlobalWanish;
    });
    
    ruCol.addEventListener("click", () => {
        rows.forEach(row => {
            entry = row.querySelectorAll("td")[1];
            if (ruGlobalWanish) {
                entry.style.color = "black";
            } else {
                entry.style.color = "white";
            };
        });
        ruGlobalWanish = !ruGlobalWanish;
    });
});