// Importer le module de configuration
import config from './config.js';
let url = "";
let columns = [];


// Garde la trace de l'objet sélectionné
let currentObjectType = '';
let currentPage = 1; // Page actuelle
const itemsPerPage = 10; // Nombre d'éléments par page
// Fonction pour ouvrir le modal avec le formulaire approprié
export function openModal() {
    document.getElementById('modal').style.display = 'block';
    const modalTitle = document.getElementById('modal-title');
    const createForm = document.getElementById('create-form');

    // Réinitialiser le formulaire
    createForm.innerHTML = '';

    // Générer le formulaire dynamique en fonction de l'objet sélectionné
    if (currentObjectType === 'customers') {
        modalTitle.innerText = 'Add New Customer';
        createForm.innerHTML = `
            <label for="name">Name:</label>
            <input type="text" id="name" name="name"><br><br>
            <label for="email">Email:</label>
            <input type="text" id="email" name="email"><br><br>
        `;
    } else if (currentObjectType === 'accounts') {
        modalTitle.innerText = 'Add New Account';
        createForm.innerHTML = `
            <label for="balance">Balance:</label>
            <input type="number" id="balance" name="balance"><br><br>
            <label for="customer_id">Customer ID:</label>
            <input type="number" id="customer_id" name="customer_id"><br><br>
        `;
    } else if (currentObjectType === 'cards') {
        modalTitle.innerText = 'Add New Card';
        createForm.innerHTML = `
            <label for="card_number">Card Number:</label>
            <input type="text" id="card_number" name="card_number"><br><br>
            <label for="account_id">Account ID:</label>
            <input type="number" id="account_id" name="account_id"><br><br>
            <label for="pin">PIN:</label>
            <input type="number" id="pin" name="pin"><br><br>
        `;
    } 
}

// Fonction pour fermer le modal
export function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Fonction pour soumettre le formulaire
export function submitForm() {
    const form = document.getElementById('create-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    let url = "";

    // Vérifiez que currentObjectType est bien défini
    console.log(`Submitting data for: ${currentObjectType}`);

    if (currentObjectType === "customers") {
        url = `${config.core_banking_url}/customers/`;
        //url= `${config.core_banking_url}/customers/`;
    } else if (currentObjectType === "accounts") {
        url = `${config.core_banking_url}/accounts/`;
    } else if (currentObjectType === "cards") {
        url = `${config.core_banking_url}/cards/`;
    } else if (currentObjectType === "transactions") {
        url = `${config.core_banking_url}/transactions/`;
    } else if (currentObjectType === "NI transactions") {
        url = `${config.ni_url}/transactions/`;
    }
    

    // Assurez-vous que l'URL est correcte
    console.log(`Sending POST request to: ${url} with data:`, data);

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Success:", data);
        closeModal(); // Fermer le modal après succès
        loadTable(currentObjectType); // Recharger les données dans le tableau
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

// Fonction pour charger les clients
window.loadCustomers = function() {
    currentObjectType = "customers";
    loadTable(currentObjectType);
};

// Fonction pour charger les comptes
window.loadAccounts = function() {
    currentObjectType = "accounts";
    loadTable(currentObjectType);
};

// Fonction pour charger les cartes
window.loadCards = function() {
    currentObjectType = "cards";
    loadTable(currentObjectType);
};

// Fonction pour charger les transactions
window.loadTransactions = function() {
    currentObjectType = "transactions";
    loadTable(currentObjectType);
};

// Fonction pour charger les transactions
window.loadNiTransactions = function() {
    currentObjectType = "NI transactions";
    loadTable(currentObjectType);
};


// Fonction pour charger les données dans le tableau en fonction du type
export function loadTable(type) {
    
    currentObjectType = type;
    const addButton = document.getElementById('add-button');
    addButton.style.display = 'block';

    // Modifier le texte du bouton en fonction de l'objet sélectionné
    if (currentObjectType === "customers") {
        url = `${config.core_banking_url}/customers/`;
        //url= `${config.core_banking_url}/customers/`;
    } else if (currentObjectType === "accounts") {
        url = `${config.core_banking_url}/accounts/`;
    } else if (currentObjectType === "cards") {
        url = `${config.core_banking_url}/cards/`;
    } else if (currentObjectType === "transactions") {
        url = `${config.core_banking_url}/transactions/`;
    } else if (currentObjectType === "NI transactions") {
        url = `${config.ni_url}/transactions/`;
    }   
 

    if (type === "customers") {
        url = `${config.core_banking_url}/customers/?skip=${(currentPage - 1) * itemsPerPage}&limit=${itemsPerPage}`;
        columns = ["id", "name", "email"];
        document.getElementById("table-title").textContent = "Customers Data Table";
    } else if (type === "accounts") {
        url = `${config.core_banking_url}/accounts/?skip=${(currentPage - 1) * itemsPerPage}&limit=${itemsPerPage}`;
        columns = ["id", "balance", "customer_id"];
        document.getElementById("table-title").textContent = "Accounts Data Table";
    } else if (type === "cards") {
        url = `${config.core_banking_url}/cards/?skip=${(currentPage - 1) * itemsPerPage}&limit=${itemsPerPage}`;
        columns = ["id", "card_number", "account_id"];
        document.getElementById("table-title").textContent = "Cards Data Table";
    } else if (type === "transactions") {
        url = `${config.core_banking_url}/transactions/?skip=${(currentPage - 1) * itemsPerPage}&limit=${itemsPerPage}`;
        columns = ["id", "account_id", "amount", "transaction_type", "status", "message", "timestamp"];
        document.getElementById("table-title").textContent = "Transactions Data Table";
    }else if (type === "NI transactions") {
        url = `${config.ni_url}/transactions/?skip=${(currentPage - 1) * itemsPerPage}&limit=${itemsPerPage}`;
        columns = ["transaction_id", "card_number", "amount", "atm_id", "transaction_type", "status", "message", "timestamp"];
        document.getElementById("table-title").textContent = "NI Transactions Data Table";
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            populateTable(data, columns);
        });
}


// Fonction pour naviguer à la page précédente
export function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadTable(currentObjectType);
    }
}

// Fonction pour naviguer à la page suivante
export function nextPage() {
    currentPage++;
    loadTable(currentObjectType);
}
// Fonction pour capitaliser la première lettre d'un mot
export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


// Fonction pour remplir le tableau
export function populateTable(data, columns) {
    const tableHeaders = document.getElementById("table-headers");
    const tableBody = document.getElementById("data-table").querySelector("tbody");

    // Mettre à jour les en-têtes du tableau
    tableHeaders.innerHTML = "";
    columns.forEach(col => {
        const th = document.createElement("th");
        th.textContent = capitalizeFirstLetter(col.replace('_', ' '));
        tableHeaders.appendChild(th);
    });

    // Mettre à jour le corps du tableau
    tableBody.innerHTML = ""; // Effacer le tableau
    data.forEach(item => {
        const row = tableBody.insertRow();
        columns.forEach(col => {
            const cell = row.insertCell();
            cell.textContent = item[col];
        });
    });
}

// Ajouter les boutons de navigation
document.getElementById('pagination').innerHTML = `
    <button onclick="previousPage()">Previous</button>
    <span>Page ${currentPage}</span>
    <button onclick="nextPage()">Next</button>
`;

// Charger les clients par défaut au chargement de la page
loadCustomers();
// Charger les clients par défaut au chargement de la page
//loadTable("customers");
//window.loadAtmTransactions = loadCustomers();
//window.showTransactionForm = loadNiTransactions();

window.submitForm = submitForm;

window.onload = function() {
    window.openModal = openModal;
    window.closeModal = closeModal;
    window.nextPage = nextPage;
    window.previousPage = previousPage;
    
};