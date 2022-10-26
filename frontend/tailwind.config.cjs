const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			width: {
				// every 8 unit = 2 rem
				'104': '26rem',
				'112': '28rem',
				'120': '30rem',
				'128': '32rem',
			},
			borderWidth: {
				// default only has even numbers from 0 to 8
				'1': '1px',
				'3': '3px',
				'5': '5px',
				'7': '7px',
			}
		}
	},

	plugins: []
};

module.exports = config;
