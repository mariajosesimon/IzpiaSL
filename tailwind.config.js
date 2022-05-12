module.exports = {
  content: ["./static/src/*.{js,css,html}"],
  theme: {
    container:{
      center:true,
    },
    extend: {},
    screens: {
      'sm': '640px',
      // => @media (min-width: 640px) { ... }

      'md': '768px',
      // => @media (min-width: 768px) { ... }

      'lg': '1024px',
      // => @media (min-width: 1024px) { ... }

      'xl': '1280px',
      // => @media (min-width: 1280px) { ... }

      '2xl': '1536px',
      // => @media (min-width: 1536px) { ... }
    }
  },
  plugins: [    plugin(function({ addComponents }){
    const buttons = {
      '.btn-red': {
        padding: '.5rem 1rem',
        borderRadius: '.25rem',
        fontWeight: '600',
        backgroundColor: '#e3342f',
        color: '#fff',
        '&:hover': {
          backgroundColor: '#cc1f1a'


         
        }
      }
    }
    
    addComponents(buttons)
  })],
}
