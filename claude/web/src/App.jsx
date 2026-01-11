import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler
} from 'chart.js'
import { Bar, Doughnut, Radar } from 'react-chartjs-2'
import './App.css'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler
)

// ═══════════════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════════════

function Header() {
  return (
    <header className="header animate-in">
      <div className="header-content">
        <h1>🎓 Student Dropout Prediction</h1>
        <p>Machine Learning Model Results Dashboard</p>
        <div className="header-badge">
          <span>📊</span>
          <span>Powered by ML Analytics</span>
        </div>
      </div>
    </header>
  )
}

function MetricCard({ label, value, description, type, icon, delay }) {
  return (
    <div className={`metric-card ${type} animate-in delay-${delay}`}>
      <div className={`metric-icon ${type}`}>{icon}</div>
      <div className="metric-label">{label}</div>
      <div className={`metric-value ${type}`}>{(value * 100).toFixed(1)}%</div>
      <div className="metric-description">{description}</div>
    </div>
  )
}

function MetricsSection({ metrics }) {
  const metricsConfig = [
    { key: 'macro_f1_score', label: 'Macro F1-Score', description: 'Primary metric - average F1 across all classes', type: 'primary', icon: '🎯' },
    { key: 'weighted_f1_score', label: 'Weighted F1-Score', description: 'F1 weighted by class support', type: 'primary', icon: '⚖️' },
    { key: 'balanced_accuracy', label: 'Balanced Accuracy', description: 'Accuracy adjusted for class imbalance', type: 'success', icon: '📈' },
    { key: 'accuracy', label: 'Accuracy', description: 'Overall correct predictions', type: 'success', icon: '✅' }
  ]

  return (
    <section className="metrics-grid">
      {metricsConfig.map((m, i) => (
        <MetricCard
          key={m.key}
          label={m.label}
          value={metrics[m.key]}
          description={m.description}
          type={m.type}
          icon={m.icon}
          delay={i + 1}
        />
      ))}
    </section>
  )
}

function ConfusionMatrix({ matrixData }) {
  const { matrix, labels } = matrixData

  return (
    <div className="card animate-in delay-1">
      <div className="card-header">
        <div className="card-icon primary">📊</div>
        <h2 className="card-title">Confusion Matrix</h2>
      </div>
      <table className="matrix-table">
        <thead>
          <tr>
            <th></th>
            {labels.map(label => <th key={label}>{label}</th>)}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => (
            <tr key={labels[i]}>
              <td className="matrix-label">{labels[i]}</td>
              {row.map((val, j) => (
                <td key={j} className={i === j ? 'matrix-diagonal' : 'matrix-off-diagonal'}>
                  {val}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function PredictionsChart({ matrixData }) {
  const { matrix, labels } = matrixData
  
  const correct = matrix.map((row, i) => row[i])
  const incorrect = matrix.map((row, i) => row.reduce((a, b) => a + b, 0) - row[i])

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Correct',
        data: correct,
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2,
        borderRadius: 6,
      },
      {
        label: 'Incorrect',
        data: incorrect,
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2,
        borderRadius: 6,
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: { color: '#94a3b8', font: { family: 'Inter', weight: 500 } }
      }
    },
    scales: {
      x: {
        stacked: true,
        ticks: { color: '#94a3b8', font: { family: 'Inter' } },
        grid: { color: 'rgba(148, 163, 184, 0.1)' }
      },
      y: {
        stacked: true,
        ticks: { color: '#94a3b8', font: { family: 'Inter' } },
        grid: { color: 'rgba(148, 163, 184, 0.1)' }
      }
    }
  }

  return (
    <div className="card animate-in delay-2">
      <div className="card-header">
        <div className="card-icon success">📈</div>
        <h2 className="card-title">Predictions Distribution</h2>
      </div>
      <div className="chart-container">
        <Bar data={data} options={options} />
      </div>
    </div>
  )
}

function PerClassMetrics({ perClassMetrics }) {
  const classStyles = {
    'Dropout': 'dropout',
    'Enrolled': 'enrolled',
    'Graduate': 'graduate'
  }

  const getProgressClass = (value) => {
    if (value >= 0.7) return 'good'
    if (value >= 0.5) return 'medium'
    return 'low'
  }

  return (
    <div className="card full-width animate-in delay-3">
      <div className="card-header">
        <div className="card-icon warning">🎯</div>
        <h2 className="card-title">Per-Class Performance Metrics</h2>
      </div>
      <table className="metrics-table">
        <thead>
          <tr>
            <th>Class</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1-Score</th>
            <th>Support</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(perClassMetrics).map(([className, metrics]) => (
            <tr key={className}>
              <td>
                <span className={`class-badge ${classStyles[className]}`}>
                  {className === 'Dropout' && '⚠️'}
                  {className === 'Enrolled' && '📚'}
                  {className === 'Graduate' && '🎓'}
                  {className}
                </span>
              </td>
              <td>
                <div className="progress-cell">
                  <div className="progress-bar">
                    <div 
                      className={`progress-fill ${getProgressClass(metrics.precision)}`}
                      style={{ width: `${metrics.precision * 100}%` }}
                    />
                  </div>
                  <span className="progress-value">{(metrics.precision * 100).toFixed(1)}%</span>
                </div>
              </td>
              <td>
                <div className="progress-cell">
                  <div className="progress-bar">
                    <div 
                      className={`progress-fill ${getProgressClass(metrics.recall)}`}
                      style={{ width: `${metrics.recall * 100}%` }}
                    />
                  </div>
                  <span className="progress-value">{(metrics.recall * 100).toFixed(1)}%</span>
                </div>
              </td>
              <td>
                <div className="progress-cell">
                  <div className="progress-bar">
                    <div 
                      className={`progress-fill ${getProgressClass(metrics.f1_score)}`}
                      style={{ width: `${metrics.f1_score * 100}%` }}
                    />
                  </div>
                  <span className="progress-value">{(metrics.f1_score * 100).toFixed(1)}%</span>
                </div>
              </td>
              <td style={{ fontWeight: 600 }}>{metrics.support}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function F1DoughnutChart({ perClassMetrics }) {
  const labels = Object.keys(perClassMetrics)
  const f1Scores = labels.map(l => perClassMetrics[l].f1_score)

  const colors = {
    'Dropout': { bg: 'rgba(239, 68, 68, 0.8)', border: '#f87171' },
    'Enrolled': { bg: 'rgba(245, 158, 11, 0.8)', border: '#fbbf24' },
    'Graduate': { bg: 'rgba(16, 185, 129, 0.8)', border: '#34d399' }
  }

  const data = {
    labels,
    datasets: [{
      data: f1Scores,
      backgroundColor: labels.map(l => colors[l].bg),
      borderColor: labels.map(l => colors[l].border),
      borderWidth: 3,
      hoverOffset: 8
    }]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '60%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: { 
          color: '#94a3b8', 
          padding: 20,
          font: { family: 'Inter', weight: 500, size: 12 }
        }
      },
      tooltip: {
        callbacks: {
          label: (ctx) => `${ctx.label}: ${(ctx.raw * 100).toFixed(1)}%`
        }
      }
    }
  }

  return (
    <div className="card animate-in delay-1">
      <div className="card-header">
        <div className="card-icon primary">📉</div>
        <h2 className="card-title">F1-Score by Class</h2>
      </div>
      <div className="chart-container chart-container-small">
        <Doughnut data={data} options={options} />
      </div>
    </div>
  )
}

function RadarChart({ perClassMetrics }) {
  const labels = Object.keys(perClassMetrics)

  const colors = {
    'Dropout': { bg: 'rgba(239, 68, 68, 0.2)', border: '#ef4444' },
    'Enrolled': { bg: 'rgba(245, 158, 11, 0.2)', border: '#f59e0b' },
    'Graduate': { bg: 'rgba(16, 185, 129, 0.2)', border: '#10b981' }
  }

  const data = {
    labels: ['Precision', 'Recall', 'F1-Score'],
    datasets: labels.map(label => ({
      label,
      data: [
        perClassMetrics[label].precision,
        perClassMetrics[label].recall,
        perClassMetrics[label].f1_score
      ],
      backgroundColor: colors[label].bg,
      borderColor: colors[label].border,
      borderWidth: 2,
      pointBackgroundColor: colors[label].border,
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 4
    }))
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { 
          color: '#94a3b8', 
          padding: 15,
          font: { family: 'Inter', weight: 500, size: 12 }
        }
      }
    },
    scales: {
      r: {
        min: 0,
        max: 1,
        ticks: { 
          color: '#64748b',
          backdropColor: 'transparent',
          font: { size: 10 }
        },
        grid: { color: 'rgba(148, 163, 184, 0.15)' },
        pointLabels: { 
          color: '#94a3b8',
          font: { family: 'Inter', size: 11, weight: 500 }
        }
      }
    }
  }

  return (
    <div className="card animate-in delay-2">
      <div className="card-header">
        <div className="card-icon success">⚖️</div>
        <h2 className="card-title">Precision vs Recall</h2>
      </div>
      <div className="chart-container chart-container-small">
        <Radar data={data} options={options} />
      </div>
    </div>
  )
}

function InterpretationCard() {
  const insights = [
    { icon: '🎯', text: <><strong>Macro F1-Score (70.6%):</strong> Durchschnittliche Performance über alle drei Klassen. Ein Wert über 70% zeigt eine gute Balance zwischen Precision und Recall.</> },
    { icon: '📊', text: <><strong>Confusion Matrix:</strong> Die Diagonale zeigt korrekte Vorhersagen. Je höher die Werte auf der Diagonale, desto besser performt das Modell.</> },
    { icon: '🎓', text: <><strong>Graduate (85.6% F1):</strong> Das Modell erkennt erfolgreiche Absolventen am besten - logisch, da dies die größte Klasse im Dataset ist.</> },
    { icon: '📚', text: <><strong>Enrolled (47.8% F1):</strong> Schwächste Performance bei noch eingeschriebenen Studenten. Diese Klasse ist am schwierigsten vorherzusagen, da sie eine Übergangsphase darstellt.</> },
    { icon: '⚠️', text: <><strong>Dropout (78.3% F1):</strong> Gute Erkennung von gefährdeten Studenten - wichtig für frühzeitige Intervention und Unterstützungsmaßnahmen.</> }
  ]

  return (
    <div className="card interpretation-card full-width animate-in delay-3">
      <div className="card-header">
        <div className="card-icon warning">📖</div>
        <h2 className="card-title">How to Interpret These Results</h2>
      </div>
      <ul className="interpretation-list">
        {insights.map((item, i) => (
          <li key={i}>
            <div className="interpretation-icon">{item.icon}</div>
            <div className="interpretation-text">{item.text}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}

function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p className="loading-text">Loading ML Results...</p>
    </div>
  )
}

function Error({ message }) {
  return (
    <div className="error-container">
      <h3>⚠️ Error Loading Data</h3>
      <p>{message}</p>
    </div>
  )
}

function Footer() {
  return (
    <footer className="footer">
      <p>🎓 Student Dropout Prediction Dashboard</p>
      <p>Machine Learning Results Visualization • Created by Claude AI</p>
    </footer>
  )
}

// ═══════════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════════

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('/result.json')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const json = await response.json()
        setData(json)
      } catch (err) {
        setError(`Failed to load result.json: ${err.message}`)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <Loading />
  if (error) return <Error message={error} />

  return (
    <div className="app-container">
      <Header />
      
      <MetricsSection metrics={data.evaluation_metrics} />
      
      <div className="dashboard-grid">
        <ConfusionMatrix matrixData={data.confusion_matrix} />
        <PredictionsChart matrixData={data.confusion_matrix} />
      </div>
      
      <PerClassMetrics perClassMetrics={data.per_class_metrics} />
      
      <div className="dashboard-grid">
        <F1DoughnutChart perClassMetrics={data.per_class_metrics} />
        <RadarChart perClassMetrics={data.per_class_metrics} />
      </div>
      
      <InterpretationCard />
      
      <Footer />
    </div>
  )
}

export default App
