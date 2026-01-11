import React, { useEffect, useState } from 'react'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend,
  PointElement,
  LineElement
} from 'chart.js'
import { Bar } from 'react-chartjs-2'
import { motion } from 'framer-motion'
import { 
  Target, 
  BarChart3, 
  Clock, 
  Settings, 
  CheckCircle2, 
  AlertCircle,
  Activity,
  Award
} from 'lucide-react'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement
)

interface MetricDetails {
  precision: number;
  recall: number;
  'f1-score': number;
  support: number;
}

interface ResultData {
  metrics: {
    accuracy: number;
    macro_f1: number;
    weighted_f1: number;
    balanced_accuracy: number;
  };
  confusion_matrix: number[][];
  classification_report: {
    [key: string]: MetricDetails;
  };
  training_time: number;
  best_params: Record<string, any>;
}

const App = () => {
  const [data, setData] = useState<ResultData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/result.json')
      .then(res => {
        if (!res.ok) throw new Error('Result file not found. Ensure "npm run dev" is running.')
        return res.json()
      })
      .then(json => {
        setData(json)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="loader"><Activity className="animate-spin mr-2" /> Loading Results...</div>
  if (error) return <div className="loader text-danger"><AlertCircle className="mr-2" /> Error: {error}</div>
  if (!data) return null

  const classes = ['Dropout', 'Enrolled', 'Graduate']
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'bottom' as const, labels: { color: '#94a3b8' } },
      tooltip: {
        backgroundColor: '#1e293b',
        titleColor: '#f1f5f9',
        bodyColor: '#cbd5e1',
        borderColor: '#334155',
        borderWidth: 1
      }
    },
    scales: {
      y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' }, beginAtZero: true, max: 1 },
      x: { grid: { display: false as const }, ticks: { color: '#94a3b8' } }
    }
  }

  const barData = {
    labels: classes,
    datasets: [
      {
        label: 'Precision',
        data: classes.map(c => data.classification_report[c].precision),
        backgroundColor: '#6366f1'
      },
      {
        label: 'Recall',
        data: classes.map(c => data.classification_report[c].recall),
        backgroundColor: '#10b981'
      },
      {
        label: 'F1-Score',
        data: classes.map(c => data.classification_report[c]['f1-score']),
        backgroundColor: '#f59e0b'
      }
    ]
  }

  return (
    <div className="dashboard-container">
      <motion.header 
        className="header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="header-title">
          <h1>Student Dropout Prediction</h1>
          <p>Advanced Academic Analytics Dashboard</p>
        </div>
        <div>
          <span className="metadata-item">
            <CheckCircle2 color="#10b981" /> System Ready
          </span>
        </div>
      </motion.header>

      <section className="metrics-grid">
        <MetricCard 
          icon={<Award />} 
          label="Accuracy" 
          value={`${(data.metrics.accuracy * 100).toFixed(1)}%`} 
          delay={0.1}
        />
        <MetricCard 
          icon={<Target />} 
          label="Macro F1" 
          value={data.metrics.macro_f1.toFixed(3)} 
          delay={0.2}
        />
        <MetricCard 
          icon={<BarChart3 />} 
          label="Weighted F1" 
          value={data.metrics.weighted_f1.toFixed(3)} 
          delay={0.3}
        />
        <MetricCard 
          icon={<Activity />} 
          label="Balanced Accuracy" 
          value={data.metrics.balanced_accuracy.toFixed(3)} 
          delay={0.4}
        />
      </section>

      <div className="grid-2">
        <motion.div 
          className="card chart-box"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h3>Per-Class Performance Comparison</h3>
          <div style={{ flex: 1, position: 'relative' }}>
            <Bar data={barData} options={chartOptions} />
          </div>
        </motion.div>

        <motion.div 
          className="card"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <h3>Confusion Matrix</h3>
          <div className="cm-table-wrapper">
            <table className="cm-table">
              <thead>
                <tr>
                  <th></th>
                  {classes.map(c => <th key={c}>Pred {c}</th>)}
                </tr>
              </thead>
              <tbody>
                {data.confusion_matrix.map((row, i) => (
                  <tr key={i}>
                    <th>True {classes[i]}</th>
                    {row.map((val, j) => (
                      <td key={j} className={`cm-cell ${i === j ? 'cm-cell-highlight' : ''}`}>
                        {val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>

      <motion.footer 
        className="metadata-footer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        <div className="metadata-item">
          <Clock size={16} /> <span>Training Time: <strong>{data.training_time.toFixed(2)}s</strong></span>
        </div>
        <div className="metadata-item">
          <Settings size={16} /> <span>Optimal Split: <strong>5 samples</strong></span>
        </div>
        <div className="metadata-item">
          <AlertCircle size={16} /> <span>Model: <strong>RandomForest (200 est.)</strong></span>
        </div>
      </motion.footer>
    </div>
  )
}

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  delay: number;
}

const MetricCard: React.FC<MetricCardProps> = ({ icon, label, value, delay }) => (
  <motion.div 
    className="card metric-card"
    initial={{ opacity: 0, scale: 0.9 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ delay }}
  >
    <div className="metric-icon">{icon}</div>
    <div className="metric-label">{label}</div>
    <div className="metric-value">{value}</div>
  </motion.div>
)

export default App
