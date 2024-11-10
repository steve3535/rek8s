// Importer le module de configuration
import config from './config.js';


// Variables globales
let currentObjectType = '';
let currentPage = 1;
const itemsPerPage = 7;

// Fonction pour ouvrir le modal avec un message
export function showTransactionModal(message) {
    document.getElementById('transaction-message').innerText = message;
    document.getElementById('transaction-modal').style.display = 'block';
}

// Fonction pour fermer le modal
export function closeTransactionModal() {
    document.getElementById('transaction-modal').style.display = 'none';
}

// Fonction pour fermer le modal
export function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Fonction pour soumettre le formulaire de transaction
export function submitTransactionForm() {
    const form = document.getElementById('transaction-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    //const url = "http://127.0.0.1:8001/withdraw/";
    const url = `${config.atm_url}/withdraw/`;
    

   

    // Nettoyer le message précédent
    //document.getElementById('response-message').innerText = '';

  
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.detail || 'Transaction failed');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("Transaction :", data);
        // Afficher le message dans le modal
        showTransactionModal(`Transaction: ${data.message}`);
        // Masquer le formulaire et recharger la liste des transactions
        document.getElementById('transaction-form-container').style.display = 'none';
        document.getElementById('data-table').style.display = 'block'; // Afficher le tableau après soumission
        document.getElementById('pagination').style.display = 'block'; // Réafficher la pagination
        loadTable('transactions');
    })
    .catch((error) => {
        console.error("Transaction Error:", error);
        // Afficher le message d'erreur dans le modal
        showTransactionModal(`Transaction Failed: ${error.message}`);
    });
}



// Fonction pour charger les transactions
export function loadAtmTransactions() {
    document.getElementById('transaction-form-container').style.display = 'none';
    document.getElementById('data-table').style.display = 'block';
    document.getElementById('pagination').style.display = 'block';
    loadTable("transactions");
}

// Fonction pour charger les données
export function loadTable(type) {
    currentObjectType = type;
    let url = "";
    let columns = [];

    if (type === "transactions") {
        url = `${config.atm_url}/showtransactions/?skip=${(currentPage - 1) * itemsPerPage}&limit=${itemsPerPage}`;
        columns = ["transaction_id", "card_number", "amount", "atm_id", "status", "message", "timestamp"];
        document.getElementById("table-title").textContent = "Transactions";
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            populateTable(data, columns);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
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
            cell.textContent = item[col] || ""; // Affiche une chaîne vide si la valeur est undefined
        });
    });
}

// Afficher le formulaire de transaction
export function showTransactionForm() {
    document.getElementById('transaction-form-container').style.display = 'block';
    document.getElementById('data-table').style.display = 'none'; // Masquer le tableau si nécessaire
    document.getElementById("table-title").textContent = "New Transaction"
    document.getElementById('pagination').style.display = 'none';  // Masquer les boutons de pagination
    
}

// Naviguer à la page précédente
export function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadTable(currentObjectType);
    }
}

// Naviguer à la page suivante
export function nextPage() {
    currentPage++;
    loadTable(currentObjectType);
}

// Capitaliser la première lettre
export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}



// Assigner les fonctions à l'objet global

window.showTransactionForm = showTransactionForm;
window.loadAtmTransactions = loadAtmTransactions;
window.submitTransactionForm = submitTransactionForm;
window.closeTransactionModal = closeTransactionModal;


window.onload = function() {
     //showTransactionForm(); // Si vous voulez montrer le formulaire par défaut
    loadAtmTransactions(); // Si vous voulez charger les transactions au démarrage
    window.nextPage = nextPage;
    window.previousPage = previousPage;
};