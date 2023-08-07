using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MarketEye.Models
{
	public class StockData
	{
		[Key]
        public int Id { get; set; }

        public string Symbol { get; set; } = string.Empty;

		[Required]
		public string Name { get; set; } = string.Empty;

		[Required]
		public int Epochs { get; set; } = 0;

		[Required]
		public int BatchSize { get; set; } = 0;

		[Required]
		public int LookBack { get; set; } = 0;

		[Required]
		public int LstmLayers { get; set; } = 0;

		[Required]
		public int LstmNeurons { get; set; } = 0;

		[Required]
		public int DenseLayers { get; set; } = 0;


		[Required]
		public int DenseNeurons { get; set; } = 0;

		[Required]
		public double Dropout { get; set; } = 0;

		[Required]
		public double PredictedOpen { get; set; } = 0;

		[Required]
		public double PredictedHigh { get; set; } = 0;

		[Required]
		public double PredictedLow { get; set; } = 0;

		[Required]
		public double PredictedClose { get; set; } = 0;

		[Required]
		public double PredictedAdjClose { get; set; } = 0;
	}
}
