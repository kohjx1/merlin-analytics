<script>
  import chartData from '../../data/barchartData.json';
  import { BarChartSimple } from '@carbon/charts-svelte';

  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';

  let data = chartData;
</script>

<BarChartSimple
  {data}
  options={{
    title: 'Top 10 keywords',
    axes: {
      left: {
        mapsTo: 'group',
        scaleType: 'labels'
      },
      bottom: {
        mapsTo: 'value'
      }
    },
    height: '400px'
  }}
/>
