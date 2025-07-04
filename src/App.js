import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [events, setEvents] = useState([]);
  const [lastFetched, setLastFetched] = useState(null);

  const convertToIST = (utcTimestamp) => {
    const datePart = utcTimestamp.split(" - ")[0];
    const timePart = utcTimestamp.split(" - ")[1].replace(" UTC", "");
    const dateStr = `${datePart} ${timePart} UTC`;
    const date = new Date(dateStr);
    
    const istOptions = {
      timeZone: 'Asia/Kolkata',
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    };
    
    return date.toLocaleString('en-IN', istOptions);
  };

  const fetchEvents = async () => {
    try {
      const res = await fetch("https://32b8-2409-40d0-12e6-35b-f800-3383-b6fc-f4a0.ngrok-free.app/events", {
        headers: {
          'ngrok-skip-browser-warning': 'true',
          'Accept': 'application/json'
        }
      });
      let data = await res.json();
      
      data = data.map(event => ({
        ...event,
        istTimestamp: convertToIST(event.timestamp),
        sortDate: new Date(event.timestamp.replace(" UTC", ""))
      })).sort((a, b) => b.sortDate - a.sortDate);
      
      setEvents(data);
      setLastFetched(new Date());
    } catch (err) {
      console.error("Error fetching events:", err);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-container">
      <div className="repo-info">
        <div className="repo-header">
          <h2>Git Repository</h2>
          <a href="https://github.com/Noorulislam01/care-track-backend" target="_blank" rel="noopener noreferrer">
            care-track-backend
          </a>
        </div>
        <div className="branch-grid">
          <div className="branch-section">
            <span className="branch-label">Local:</span>
            <span className="branch-name">main</span>
            <span className="branch-name active">test (current)</span>
          </div>
          <div className="branch-section">
            <span className="branch-label">Remote:</span>
            <span className="branch-name">origin/main</span>
            <span className="branch-name">origin/test</span>
          </div>
        </div>
      </div>

      <div className="events-container">
        <div className="events-header">
          <h2>Event Log (IST)</h2>
          {lastFetched && (
            <span className="last-updated">
              Last updated: {lastFetched.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}
            </span>
          )}
        </div>

        <table className="events-table">
          {/* Table content remains the same */}
          <thead>
            <tr>
              <th>Timestamp (IST)</th>
              <th>Action</th>
              <th>Author</th>
              <th>From Branch</th>
              <th>To Branch</th>
              <th>Request ID</th>
            </tr>
          </thead>
          <tbody>
            {events.length > 0 ? (
              events.map((event) => (
                <tr key={event._id}>
                  <td>{event.istTimestamp}</td>
                  <td>{event.action}</td>
                  <td>{event.author}</td>
                  <td>{event.from_branch ? `${event.from_branch}` : `${event.to_branch} (local)`}</td>
                  <td>{event.to_branch}</td>
                  <td>{event.request_id}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="no-events">
                  {events.length === 0 ? "Loading events..." : "No events found"}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;