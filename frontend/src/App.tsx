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
    const websocket = new WebSocket("ws://localhost:8000/ws/telemetry");

    websocket.addEventListener("open", () => {
      console.log("WebSocket connected");
      setConnected(true);
    });

    websocket.addEventListener("close", () => {
      console.log("WebSocket closed");
      setConnected(false);
    });

    websocket.addEventListener("error", (error) => {
      console.error("WebSocket error", error);
      setConnected(false);
    });

    websocket.addEventListener("message", (event) => {
      const data: TelemetryEvent = JSON.parse(event.data);

      setEvents((previousEvents) =>
        [data, ...previousEvents]
          .filter(
            (item, index, array) =>
              array.findIndex((candidate) => candidate.id === item.id) ===
              index,
          )
          .slice(0, 50),
      );
    });

    const loadHistoricalEvents = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/api/v1/telemetry?limit=50",
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const historicalEvents: TelemetryEvent[] = await response.json();

        setEvents((previousEvents) => {
          const mergedEvents = [...previousEvents, ...historicalEvents];

          return Array.from(
            new Map(mergedEvents.map((item) => [item.id, item])).values(),
          )
            .sort(
              (a, b) =>
                new Date(b.timestamp).getTime() -
                new Date(a.timestamp).getTime(),
            )
            .slice(0, 50);
        });
      } catch (error) {
        console.error("Failed to load historical telemetry", error);
      }
    };

    void loadHistoricalEvents();

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
      is_anomaly: event.is_anomaly,
    }));

  const anomalyCount = events.filter((event) => event.is_anomaly).length;
  const normalCount = events.length - anomalyCount;
  const anomalyPercentage =
    events.length > 0
      ? ((anomalyCount / events.length) * 100).toFixed(1)
      : "0.0";

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

        <section className="grid gap-6 md:grid-cols-4">
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
            <h2 className="text-sm text-zinc-400 mb-2">Normal Events</h2>
            <p className="text-2xl font-semibold text-green-400">
              {normalCount}
            </p>
          </div>

          <div className="rounded-2xl border border-red-900 bg-red-950/30 p-6">
            <h2 className="text-sm text-red-300 mb-2">Active Anomalies</h2>
            <p className="text-2xl font-semibold text-red-400">
              {anomalyCount}
            </p>
            <p className="text-xs text-red-300 mt-1">
              {anomalyPercentage}% of visible events
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
            <h2 className="text-xl font-semibold">Live Telemetry</h2>

            <div className="flex gap-4 text-sm">
              <span className="flex items-center gap-2 text-zinc-400">
                <span className="h-2 w-2 rounded-full bg-green-400" />
                Normal
              </span>

              <span className="flex items-center gap-2 text-zinc-400">
                <span className="h-2 w-2 rounded-full bg-red-500" />
                Anomaly
              </span>
            </div>
          </div>

          <div className="h-96 min-h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid stroke="#27272a" />

                <XAxis dataKey="time" stroke="#a1a1aa" />

                <YAxis stroke="#a1a1aa" />

                <Tooltip
                  contentStyle={{
                    backgroundColor: "#18181b",
                    border: "1px solid #3f3f46",
                    borderRadius: "8px",
                    color: "#f4f4f5",
                  }}
                  formatter={(value) => [`${value} °C`, "Temperature"]}
                />

                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#4ade80"
                  strokeWidth={2}
                  dot={(props) => {
                    const { cx, cy, payload } = props;

                    if (typeof cx !== "number" || typeof cy !== "number") {
                      return <></>;
                    }

                    return (
                      <circle
                        cx={cx}
                        cy={cy}
                        r={payload.is_anomaly ? 6 : 3}
                        fill={payload.is_anomaly ? "#ef4444" : "#4ade80"}
                        stroke={payload.is_anomaly ? "#fecaca" : "#18181b"}
                        strokeWidth={2}
                      />
                    );
                  }}
                  activeDot={{ r: 7 }}
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
                  <th className="py-3 text-left">Status</th>
                  <th className="py-3 text-left">Anomaly Score</th>
                </tr>
              </thead>

              <tbody>
                {events.map((event) => (
                  <tr
                    key={event.id}
                    className={`border-b border-zinc-800 ${
                      event.is_anomaly
                        ? "bg-red-950/40 hover:bg-red-950/60"
                        : "hover:bg-zinc-800/40"
                    }`}
                  >
                    <td className="py-3 text-zinc-300">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </td>

                    <td className="py-3">{event.device_id}</td>

                    <td className="py-3">{event.metric_name}</td>

                    <td
                      className={`py-3 font-semibold ${
                        event.is_anomaly ? "text-red-400" : "text-zinc-100"
                      }`}
                    >
                      {event.metric_value}
                    </td>

                    <td className="py-3">
                      {event.is_anomaly ? (
                        <span className="rounded-full bg-red-500/20 px-3 py-1 text-xs font-semibold text-red-400">
                          ANOMALY
                        </span>
                      ) : (
                        <span className="rounded-full bg-green-500/20 px-3 py-1 text-xs font-semibold text-green-400">
                          NORMAL
                        </span>
                      )}
                    </td>

                    <td
                      className={`py-3 font-mono ${
                        event.is_anomaly ? "text-red-400" : "text-zinc-400"
                      }`}
                    >
                      {event.anomaly_score.toFixed(2)}
                    </td>
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
