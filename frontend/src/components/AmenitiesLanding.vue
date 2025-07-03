<!-- Amenities Grid View -->

<script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'

  const rooms = ref([])
  const amenities = ref([])

  onMounted(async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_BASE_URL
      const { data: roomTypes } = await axios.get(`${backendUrl}/room/get_all_room_types/`)
      
      roomTypes.sort((a, b) => a.name.localeCompare(b.name))

      rooms.value = roomTypes.map(room => ({
        type: `Type ${room.name}`,
        amenities: room.amenities.map(a => a.name)
      }))

      const allAmenities = new Set()
      roomTypes.forEach(rt => {
        rt.amenities.forEach(a => allAmenities.add(a.name))
      })
      amenities.value = Array.from(allAmenities).sort()

    } catch (error) {
      console.error('Failed to load amenities or room types:', error)
    }
  })
</script>

<template>
  <div class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg z-10">
    <h2 class="text-2xl font-bold text-center mb-6">Room Type Amenities</h2>
    <div class="overflow-x-auto">
      <table class="w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-[#09240B] text-white">
            <th class="p-4 text-left">Amenities</th>
            <th
              v-for="(room, index) in rooms"
              :key="'header-' + index"
              class="p-4 text-center"
            >
              {{ room.type }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(amenity, aIndex) in amenities"
            :key="'row-' + aIndex"
            class="border border-gray-300"
          >
            <td class="p-3 font-medium">{{ amenity }}</td>
            <td
              v-for="(room, rIndex) in rooms"
              :key="'cell-' + aIndex + '-' + rIndex"
              class="p-3 text-center"
            >
              <span v-if="room.amenities.includes(amenity)" class="text-green-500">✔</span>
              <span v-else class="text-red-500">✖</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>