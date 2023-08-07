using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MarketEye.DataAccess.Migrations
{
    /// <inheritdoc />
    public partial class addParameters : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<double>(
                name: "CurrentPrice",
                table: "StockDatas",
                type: "float",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "PredictedAdjClose",
                table: "StockDatas",
                type: "float",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "PredictedClose",
                table: "StockDatas",
                type: "float",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "PredictedHigh",
                table: "StockDatas",
                type: "float",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "PredictedLow",
                table: "StockDatas",
                type: "float",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "PredictedOpen",
                table: "StockDatas",
                type: "float",
                nullable: false,
                defaultValue: 0.0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "CurrentPrice",
                table: "StockDatas");

            migrationBuilder.DropColumn(
                name: "PredictedAdjClose",
                table: "StockDatas");

            migrationBuilder.DropColumn(
                name: "PredictedClose",
                table: "StockDatas");

            migrationBuilder.DropColumn(
                name: "PredictedHigh",
                table: "StockDatas");

            migrationBuilder.DropColumn(
                name: "PredictedLow",
                table: "StockDatas");

            migrationBuilder.DropColumn(
                name: "PredictedOpen",
                table: "StockDatas");
        }
    }
}
