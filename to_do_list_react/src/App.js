import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const API_URL = 'http://localhost:8000/api/todos/';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = () => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => setTasks(data));
  };

  const addTask = () => {
    if (!title.trim()) return;
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, completed: false })
    }).then(fetchTasks);
    setTitle("");
  };

  const deleteTask = (id) => {
    fetch(`${API_URL}${id}/`, {
      method: 'DELETE'
    }).then(fetchTasks);
  };

  const toggleComplete = (task) => {
    fetch(`${API_URL}${task.id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...task, completed: !task.completed })
    }).then(fetchTasks);
  };

  return (
    <div className="container my-5">
      <h1 className="text-center mb-4">To-Do List</h1>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter task"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button className="btn btn-primary" onClick={addTask}>Add</button>
      </div>
      <ul className="list-group">
        {tasks.map(task => (
          <li
            key={task.id}
            className={`list-group-item d-flex justify-content-between align-items-center ${task.completed ? 'list-group-item-success' : ''}`}
          >
            <div>
              <input
                type="checkbox"
                className="form-check-input me-2"
                checked={task.completed}
                onChange={() => toggleComplete(task)}
              />
              <span className={task.completed ? 'text-decoration-line-through' : ''}>
                {task.title}
              </span>
            </div>
            <button className="btn btn-sm btn-danger" onClick={() => deleteTask(task.id)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}


export default App;
