<script>
  import { BarChartSimple } from '@carbon/charts-svelte';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';
  import axios from 'axios';

  export let barChartData = [];
</script>

<BarChartSimple
  data={barChartData}
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
