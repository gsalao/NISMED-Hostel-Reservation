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

<script setup>
import { ref } from 'vue'

const rooms = ref([
  {
    type: 'Type A',
    amenities: [
      'Hot & Cold Shower',
      'Linen',
      'Towel',
      'Air-conditioning',
      'Smart TV',
      'Mini Refrigerator',
      'Private Toilet & Bath',
    ],
  },
  {
    type: 'Type B',
    amenities: [
      'Hot & Cold Shower',
      'Linen',
      'Towel',
      'Air-conditioning',
      'Ceiling Fan',
      'Shared Toilet & Bath',
    ],
  },
  {
    type: 'Type C',
    amenities: [
      'Hot & Cold Shower',
      'Linen',
      'Ceiling Fan',
      'Shared Toilet & Bath',
    ],
  },
])

const amenities = ref([
  'Hot & Cold Shower',
  'Linen',
  'Towel',
  'Air-conditioning',
  'Smart TV',
  'Mini Refrigerator',
  'Private Toilet & Bath',
  'Ceiling Fan',
  'Shared Toilet & Bath',
])
</script> 