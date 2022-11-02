<script>
  import { WordCloudChart } from '@carbon/charts-svelte';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';

  export let wordCloudData = [];
</script>

<WordCloudChart
  data={wordCloudData}
  options={{
    title: 'Word Cloud',
    resizable: true,
    color: {
      pairing: {
        option: 10
      }
    },
    height: '400px'
  }}
/>
