import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useHomePageStore = defineStore('room', () => {
  const images = ref([])
  const roomTypes = ref([])
  const rates = ref([])
  const loaded = ref(false)

  const loadAll = async () => {
    if (loaded.value) return

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_BASE_URL

      const [imagesRes, typesRes, ratesRes] = await Promise.all([
        axios.get(`${backendUrl}/room/get_all_room_type_images/`),
        axios.get(`${backendUrl}/room/get_all_room_types/`),
        axios.get(`${backendUrl}/room/get_all_room_rates/`)
      ])

      images.value = imagesRes.data
      roomTypes.value = typesRes.data
      rates.value = ratesRes.data
      loaded.value = true
    } catch (err) {
      console.error('Failed to load room data', err)
    }
  }

  const invalidate = () => {
    loaded.value = false
  }

  return { images, roomTypes, rates, loaded, loadAll, invalidate }
})