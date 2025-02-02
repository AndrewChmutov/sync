import { defineStore } from 'pinia'
import { io, Socket } from 'socket.io-client'

interface SocketState {
  socket: Socket | null
  isConnected: boolean
}

export const useSocketStore = defineStore('store', {
  state: (): SocketState => ({
    socket: null,
    isConnected: false,
  }),
  actions: {
    connect() {
      if (this.socket !== null) return

      this.socket = io(`wss://localhost:8000/ui`)
      console.log(this.socket)
      this.socket.on('connect', () => {
        if (this.socket!.recovered) {
          console.log('WebSocket reconnected')
        } else {
          console.log('WebSocket connected')
        }
      })

      this.socket.on('kek', (data) => {
        console.log('KEK RECEIVED: ', JSON.stringify(data))
      })

      this.socket.on('disconnect', () => {
        console.log('WebSocket disconnected')
      })
    },
  },
})
