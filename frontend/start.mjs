import { preview } from 'vite'

const port = parseInt(process.env.PORT) || 4173

const server = await preview({
  preview: {
    host: '0.0.0.0',
    port: port,
  },
})

console.log(`Server running on port ${port}`)
