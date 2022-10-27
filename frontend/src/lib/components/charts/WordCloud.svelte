<script>
  import { WordCloudChart } from '@carbon/charts-svelte';
  import item from '../../data/sample.json';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';

  let data = item;
</script>

<WordCloudChart
  {data}
  options={{
    title: 'Word cloud',
    resizable: true,
    color: {
      pairing: {
        option: 3
      }
    },
    height: '400px'
  }}
/>
