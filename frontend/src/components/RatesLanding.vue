<template>
  <div class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg z-10">
    <h2 class="text-2xl font-bold text-center mb-6">Room Rates Per Day</h2>
    <div class="overflow-x-auto">
      <table class="w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-[#09240B] text-white">
            <th class="p-4 text-left">Room Type</th>
            <th
              v-for="(category, index) in categories"
              :key="'header-' + index"
              class="p-4 text-center"
            >
              {{ category }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(rate, rateIndex) in rates"
            :key="'rate-' + rateIndex"
            class="border border-gray-300"
          >
            <td class="p-3 font-medium">{{ rate.type }}</td>
            <td
              v-for="(category, catIndex) in categories"
              :key="'price-' + rateIndex + '-' + catIndex"
              class="p-3 text-center"
            >
              <span v-if="rate.prices[category]" class="font-bold">
                Php {{ rate.prices[category] }}
              </span>
              <span v-else class="text-gray-400">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const categories = ref(['Single', 'Double', 'Triple'])

const rates = ref([
  { type: 'Type A', prices: { Single: 1395, Double: 1900 } },
  { type: 'Type B', prices: { Single: 1145, Double: 1785 } },
  { type: 'Type C', prices: { Single: 440, Double: 740, Triple: 925 } },
])
</script>