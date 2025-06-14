import { useState } from 'react'
import './App.css'

function App() {
  const [metrics, setMetrics] = useState(Array(18).fill(""))
  const [score, setScore] = useState("")

  const metricName = ["Timestamp", "Cpu Usage", "Cpu Frequency", "Cpu Frequency Percent", "Cpu idle time", "Cpu Temperature", "Num Cores", "Num Threads", "Load Avd 1m", "Uptime", "Memory Usage", "Swap Usage", "Disk Read Bytes", "Disk Write Bytes", "Network Sent Bytes", "Network Recieve Bytes", "Context Switches", "Interrupts", "Cpu percent per core"]

  const handleSetMetrics = (e, idx) => {
    const newMetrics = [... metrics];
    newMetrics[idx] = e.target.value;
    setMetrics(newMetrics);
    console.log(newMetrics);
  } 

  const handleGetMetrics = async () => {
    const response = await fetch("http://localhost:5000/get_metrics"); 
    const data = await response.json();
    console.log(data.metrics);
    setMetrics(data.metrics);
  }

  const handleGetScore = async () => {
    const metricJSON = {
      "metrics" : metrics
    };
    const options = {
      method: "POST",
      headers: {
                "Content-Type": "application/json"
            },
      body: JSON.stringify(metricJSON)
    }
    const response = await fetch("http://localhost:5000/get_score", options);
    const data = await response.json();
    console.log(data);
    setScore(data.score);

  }
  return (
    <>
      <form className='form-vertical'  onSubmit={e => e.preventDefault()}>
      {metrics.map((value, idx) => (
        <div className = "container" key={idx} style={{ display: "flex", alignItems: "center", marginBottom: "8px" }}>
          <label style={{ width: "120px" }}>{`${metricName[idx]}:`}</label>
          <input
            type="text"
            value={value || ""}
            onChange={e => handleSetMetrics(e, idx)}
          />
    </div>
  ))}
  <button className='get-metrics' onClick={() => handleGetMetrics()}>Get Metrics</button>
  <button className='get-score' onClick={() => handleGetScore()}>Get Score</button>
</form>
    {score && (
    <div style={{ marginTop: "24px", fontSize: "1.5em" }}>
      <strong>Score:</strong> {score}
    </div>
  )}
    </>
  )
}

export default App
