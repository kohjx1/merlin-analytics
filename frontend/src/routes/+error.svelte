<script>
    import { page } from '$app/stores';
  </script>
  
  <h1>{$page.status}: {$page.error.message}</h1>
  <h1>Invalid URL. Please check :)</h1>