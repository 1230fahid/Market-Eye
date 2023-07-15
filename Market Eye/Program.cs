using System.Configuration;
using Reddit;
using RestSharp;
using Reddit.Models.Internal;
using System.Diagnostics;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Market_Eye.Data;
using Market_Eye.Areas.Identity.Data;

var reddit = new RedditClient(appId: "EVmKnLlQ8BUIJriRiemHpw", appSecret: "duW1EV_49oA2YdQw1e1Xq2tthwPIhg", refreshToken: "563986035943-P0Vos3WT70oTDxy60XqaQv6jfPIehw");
var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("Market_EyeContextConnection") ?? throw new InvalidOperationException("Connection string 'Market_EyeContextConnection' not found.");

builder.Services.AddDbContext<Market_EyeContext>(options => options.UseSqlServer(connectionString));

builder.Services.AddDefaultIdentity<Market_EyeUser>(options => options.SignIn.RequireConfirmedAccount = true).AddEntityFrameworkStores<Market_EyeContext>();

// Add services to the container.
builder.Services.AddControllersWithViews();
//Add razor pages
builder.Services.AddRazorPages();

builder.Services.AddSingleton(reddit);


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.MapRazorPages();
app.Run();
