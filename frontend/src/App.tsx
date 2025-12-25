import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LayoutDashboard,
  CheckCircle2,
  Clock,
  Plus,
  Trash2,
  Search,
  Settings,
  Bell,
  User,
  Filter,
  MoreVertical
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'completed';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
}

const API_BASE = 'http://localhost:8000';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState('');
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('Dashboard');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await axios.get(`${API_BASE}/tasks`);
      setTasks(res.data);
    } catch (err) {
      console.error("Failed to fetch tasks", err);
      // Mock data for demo if backend is not running/connected
      setTasks([
        { id: '1', title: 'Connect Supabase URL', status: 'pending', priority: 'high', created_at: new Date().toISOString() },
        { id: '2', title: 'Setup Python Backend', status: 'completed', priority: 'medium', created_at: new Date().toISOString() },
        { id: '3', title: 'Design Glassmorphism UI', status: 'completed', priority: 'low', created_at: new Date().toISOString() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.trim()) return;

    try {
      const res = await axios.post(`${API_BASE}/tasks`, {
        title: newTask,
        status: 'pending',
        priority: 'medium'
      });
      setTasks([...tasks, res.data[0]]);
      setNewTask('');
    } catch {
      // Optimistic update for demo purposes
      const mockTask: Task = {
        id: Math.random().toString(36).substr(2, 9),
        title: newTask,
        status: 'pending',
        priority: 'medium',
        created_at: new Date().toISOString()
      };
      setTasks([...tasks, mockTask]);
      setNewTask('');
    }
  };

  const toggleTask = async (id: string) => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    try {
      await axios.put(`${API_BASE}/tasks/${id}`, {
        ...task,
        status: task.status === 'completed' ? 'pending' : 'completed'
      });
      setTasks(tasks.map(t => t.id === id ? { ...t, status: t.status === 'completed' ? 'pending' : 'completed' } : t));
    } catch {
      setTasks(tasks.map(t => t.id === id ? { ...t, status: t.status === 'completed' ? 'pending' : 'completed' } : t));
    }
  };

  const deleteTask = async (id: string) => {
    try {
      await axios.delete(`${API_BASE}/tasks/${id}`);
      setTasks(tasks.filter(t => t.id !== id));
    } catch {
      setTasks(tasks.filter(t => t.id !== id));
    }
  };

  return (
    <div className="app-container">
      {/* Background Orbs */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>

      <AnimatePresence>
        {loading && (
          <motion.div
            className="loading-overlay"
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="loader-content">
              <div className="spinner"></div>
              <p>Fetching your workspace...</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">P3</div>
          <span>Python Tier 3</span>
        </div>

        <nav className="nav-links">
          {[
            { name: 'Dashboard', icon: LayoutDashboard },
            { name: 'Tasks', icon: CheckCircle2 },
            { name: 'Timeline', icon: Clock },
            { name: 'Settings', icon: Settings },
          ].map((item) => (
            <button
              key={item.name}
              className={`nav-item ${activeTab === item.name ? 'active' : ''}`}
              onClick={() => setActiveTab(item.name)}
            >
              <item.icon size={20} />
              <span>{item.name}</span>
            </button>
          ))}
        </nav>

        <div className="user-profile">
          <div className="avatar">
            <User size={20} />
          </div>
          <div className="user-info">
            <p className="user-name">Admin User</p>
            <p className="user-status">Online</p>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="top-header">
          <div className="search-bar">
            <Search size={18} />
            <input type="text" placeholder="Search insights..." />
          </div>
          <div className="header-actions">
            <button className="icon-btn"><Bell size={20} /></button>
            <div className="divider"></div>
            <button className="premium-btn">Upgrade Plan</button>
          </div>
        </header>

        <section className="dashboard-view">
          <div className="dashboard-header">
            <div>
              <h1>Project Orchestrator</h1>
              <p className="subtitle">Manage your three-tier application logic and data.</p>
            </div>
            <button className="add-task-btn" onClick={() => (document.getElementById('task-input') as HTMLInputElement).focus()}>
              <Plus size={20} />
              <span>New Task</span>
            </button>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Tasks</span>
              <span className="stat-value">{tasks.length}</span>
              <div className="stat-graph purple"></div>
            </div>
            <div className="stat-card">
              <span className="stat-label">Completed</span>
              <span className="stat-value">{tasks.filter(t => t.status === 'completed').length}</span>
              <div className="stat-graph blue"></div>
            </div>
            <div className="stat-card">
              <span className="stat-label">Productivity</span>
              <span className="stat-value">92%</span>
              <div className="stat-graph green"></div>
            </div>
          </div>

          <div className="tasks-section">
            <div className="section-header">
              <h2>Recent Tasks</h2>
              <div className="filters">
                <button className="filter-btn"><Filter size={16} /> Filter</button>
              </div>
            </div>

            <form onSubmit={handleAddTask} className="task-form">
              <input
                id="task-input"
                type="text"
                placeholder="What needs to be done?"
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
              />
              <button type="submit"><Plus size={20} /></button>
            </form>

            <div className="tasks-list">
              <AnimatePresence>
                {tasks.map((task) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className={`task-item ${task.status}`}
                  >
                    <div className="task-checkbox" onClick={() => toggleTask(task.id)}>
                      {task.status === 'completed' && <CheckCircle2 size={16} />}
                    </div>
                    <div className="task-details">
                      <p className="task-title">{task.title}</p>
                      <span className={`priority-badge ${task.priority}`}>{task.priority}</span>
                    </div>
                    <div className="task-actions">
                      <button className="delete-btn" onClick={() => deleteTask(task.id)}>
                        <Trash2 size={16} />
                      </button>
                      <button className="more-btn"><MoreVertical size={16} /></button>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
