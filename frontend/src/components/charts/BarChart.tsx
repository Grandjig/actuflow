import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface BarChartProps {
  data: Array<Record<string, unknown>>;
  bars: Array<{
    dataKey: string;
    name: string;
    color?: string;
    stackId?: string;
  }>;
  xDataKey: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
  layout?: 'horizontal' | 'vertical';
}

const COLORS = ['#2563eb', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#0891b2'];

export default function BarChart({
  data,
  bars,
  xDataKey,
  height = 300,
  showGrid = true,
  showLegend = true,
  layout = 'horizontal',
}: BarChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsBarChart
        data={data}
        layout={layout}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        {layout === 'horizontal' ? (
          <>
            <XAxis dataKey={xDataKey} />
            <YAxis />
          </>
        ) : (
          <>
            <XAxis type="number" />
            <YAxis dataKey={xDataKey} type="category" />
          </>
        )}
        <Tooltip />
        {showLegend && <Legend />}
        {bars.map((bar, index) => (
          <Bar
            key={bar.dataKey}
            dataKey={bar.dataKey}
            name={bar.name}
            fill={bar.color || COLORS[index % COLORS.length]}
            stackId={bar.stackId}
          />
        ))}
      </RechartsBarChart>
    </ResponsiveContainer>
  );
}
