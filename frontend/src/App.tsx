import { useEffect, useState } from "react";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type TelemetryEvent = {
  id: number;
  device_id: number;
  metric_name: string;
  metric_value: number;
  timestamp: string;
  is_anomaly: boolean;
  anomaly_score: number;
};

function App() {
  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState<TelemetryEvent[]>([]);

  useEffect(() => {
    const websocket = new WebSocket("ws://127.0.0.1:8000/ws/telemetry");

    websocket.onopen = () => {
      setConnected(true);
    };

    websocket.onclose = () => {
      setConnected(false);
    };

    websocket.onmessage = (event) => {
      const data: TelemetryEvent = JSON.parse(event.data);

      setEvents((previousEvents) => [data, ...previousEvents].slice(0, 50));
    };

    return () => {
      websocket.close();
    };
  }, []);

  const chartData = events
    .slice()
    .reverse()
    .map((event) => ({
      time: new Date(event.timestamp).toLocaleTimeString(),
      value: event.metric_value,
    }));

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold">
            Real-Time IoT Anomaly Detection
          </h1>

          <p className="text-zinc-400 mt-2">
            MQTT telemetry streaming with anomaly detection
          </p>
        </header>

        <section className="grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-sm text-zinc-400 mb-2">WebSocket Status</h2>

            <p
              className={`text-2xl font-semibold ${
                connected ? "text-green-400" : "text-red-400"
              }`}
            >
              {connected ? "Connected" : "Disconnected"}
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-sm text-zinc-400 mb-2">Total Events</h2>

            <p className="text-2xl font-semibold">{events.length}</p>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-sm text-zinc-400 mb-2">Active Anomalies</h2>

            <p className="text-2xl font-semibold text-yellow-400">
              {events.filter((event) => event.is_anomaly).length}
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          <h2 className="text-xl font-semibold mb-4">Live Telemetry</h2>

          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid stroke="#27272a" />

                <XAxis dataKey="time" stroke="#a1a1aa" />

                <YAxis stroke="#a1a1aa" />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#4ade80"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Events</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-zinc-400">
                <tr className="border-b border-zinc-800">
                  <th className="py-3 text-left">Time</th>
                  <th className="py-3 text-left">Device</th>
                  <th className="py-3 text-left">Metric</th>
                  <th className="py-3 text-left">Value</th>
                  <th className="py-3 text-left">Anomaly</th>
                  <th className="py-3 text-left">Score</th>
                </tr>
              </thead>

              <tbody>
                {events.map((event) => (
                  <tr
                    key={event.id}
                    className={`border-b border-zinc-800 ${
                      event.is_anomaly ? "bg-red-950/40" : ""
                    }`}
                  >
                    <td className="py-3 text-zinc-300">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </td>

                    <td className="py-3">{event.device_id}</td>

                    <td className="py-3">{event.metric_name}</td>

                    <td className="py-3">{event.metric_value}</td>

                    <td className="py-3">
                      {event.is_anomaly ? "Yes" : "No"}
                    </td>

                    <td className="py-3">{event.anomaly_score.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  );
}

export default App;