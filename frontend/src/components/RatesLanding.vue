<!-- Room Rates Grid View -->

<script setup>
  import { computed } from 'vue'
  import { useHomePageStore } from '../stores/homePageStore'

  const store = useHomePageStore()

  const categories = ['Single', 'Double', 'Triple']

  const rates = computed(() => {
    const grouped = {}

    store.rates.forEach(rate => {
      const type = rate.room_type
      const typeAlpha =
        type === 1 ? 'Type C' : type === 2 ? 'Type B' : 'Type A'
      const occ = rate.occupancy
      const label =
        occ === 1 ? 'Single' : occ === 2 ? 'Double' : 'Triple'

      if (!grouped[typeAlpha]) grouped[typeAlpha] = {}
      grouped[typeAlpha][label] = parseFloat(rate.rate)
    })

    const sortedEntries = Object.entries(grouped).sort((a, b) =>
      a[0].localeCompare(b[0])
    )

    return sortedEntries.map(([type, prices]) => ({
      type,
      prices
    }))
  })
</script>

<template>
  <div class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg z-10">
    <h2 class="text-2xl font-bold text-center mb-6">Room Rates Per Night</h2>
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