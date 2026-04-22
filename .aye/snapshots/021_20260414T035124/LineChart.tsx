import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface LineChartProps {
  data: Array<Record<string, unknown>>;
  lines: Array<{
    dataKey: string;
    name: string;
    color?: string;
    strokeDasharray?: string;
  }>;
  xDataKey: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
}

const COLORS = ['#2563eb', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#0891b2'];

export default function LineChart({
  data,
  lines,
  xDataKey,
  height = 300,
  showGrid = true,
  showLegend = true,
}: LineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis dataKey={xDataKey} />
        <YAxis />
        <Tooltip />
        {showLegend && <Legend />}
        {lines.map((line, index) => (
          <Line
            key={line.dataKey}
            type="monotone"
            dataKey={line.dataKey}
            name={line.name}
            stroke={line.color || COLORS[index % COLORS.length]}
            strokeDasharray={line.strokeDasharray}
            dot={false}
          />
        ))}
      </RechartsLineChart>
    </ResponsiveContainer>
  );
}
