
let input=document.querySelector("#input");

let button =document.querySelector("#add");

let list = document.querySelector("#list");
let tasks = []; 
let deadlineInput = document.querySelector('#deadline');

button.addEventListener("click",addTask);

function addTask(){

    let data =input.value.trim();

    if(!data){
        alert("Please Enter Your Task");
        return;
    }

const taskObj = {
        id: Date.now(),
        text: data,
        priority: 'medium',
        deadline: deadlineInput.value || '',        
        completed: false
    };
 

    tasks.push(taskObj);
    
    renderList();
    updateCounters();
    input.value = "";
    deadlineInput.value = "";
}


function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        renderList();
       
         updateCounters();
    }
}

function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    renderList();
   
    updateCounters();
}

function renderList() {
    list.innerHTML = tasks.map(task => `
        <li onclick="toggleTask(${task.id})" style="${task.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}">
            <span style="cursor: pointer; padding: 10px; display: block;">${task.text}</span>
            <button onclick="toggleTask(${task.id}); event.stopPropagation();" style="margin-right: 5px;">${task.completed ? 'Undo' : 'Done'}</button>
            <button onclick="deleteTask(${task.id}); event.stopPropagation();">🗑</button>
        </li>
    `).join('');
}

let currentFilter = 'all';
let currentSort = 'priority';
let debounceTimer;


let filterBtns = document.querySelectorAll('.filter-btn'); 
let sortSelect = document.querySelector('#sort'); 
let searchInput = document.querySelector('#search'); 

filterBtns.forEach(btn => btn.addEventListener('click', setFilter));
sortSelect?.addEventListener('change', () => { currentSort = sortSelect.value; renderList(); });
searchInput?.addEventListener('input', debounceSearch);


function setFilter(e) {
    currentFilter = e.target.textContent.includes('All') ? 'all' : 
                   e.target.textContent.includes('Completed') ? 'completed' : 'pending';
    renderList();
}

function debounceSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        renderList();
    }, 300);
}

function sortTasks(taskList) {
    let sorted = [...taskList];
    if (currentSort === 'priority') {
        sorted.sort((a, b) => getPriorityValue(b.priority) - getPriorityValue(a.priority));
    } else if (currentSort === 'deadline') {
        sorted.sort((a, b) => {
            if (!a.deadline) return 1;
            if (!b.deadline) return -1;
            return new Date(a.deadline) - new Date(b.deadline);
        });
    }
    return sorted;
}

function getPriorityValue(prio) {
    const values = { high: 3, medium: 2, low: 1 };
    return values[prio] || 1;
}

function renderList() {
    
    let filtered = tasks.filter(task => {
        const search = searchInput?.value.toLowerCase() || '';
        const matchesSearch = task.text.toLowerCase().includes(search);
        
        if (currentFilter === 'completed') return task.completed && matchesSearch;
        if (currentFilter === 'pending') return !task.completed && matchesSearch;
        return matchesSearch;
    });
    
    // Sort
    filtered = sortTasks(filtered);
    
    // Render
   list.innerHTML = filtered.map(task => {
    const overdue = task.deadline && new Date(task.deadline) < new Date();
    const overdueStyle = overdue ? 'border-left: 5px solid red; background: #ffebee;' : '';
    
    return `
        <li onclick="toggleTask(${task.id})" style="${task.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''} ${overdueStyle}">
            <span style="cursor: pointer; padding: 10px; display: block;">
                ${task.text} ${overdue ? '<strong style="color: red;"> (OVERDUE)</strong>' : ''}
            </span>
            <button onclick="toggleTask(${task.id}); event.stopPropagation();" style="margin-right: 5px;">${task.completed ? 'Undo' : 'Done'}</button>
            <button onclick="deleteTask(${task.id}); event.stopPropagation();">🗑</button>
        </li>
    `;
}).join('');

}

let counterDiv = document.querySelector('.container h5');
function updateCounters() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;
    
    counterDiv.innerHTML = 
        `Total Tasks: <strong>${total}</strong> | ` +
        `Completed Tasks: <strong>${completed}</strong> | ` +
        `Pending Tasks: <strong>${pending}</strong>`;
}

renderList();
updateCounters();

