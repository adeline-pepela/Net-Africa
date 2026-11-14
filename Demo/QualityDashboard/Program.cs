using QualityDashboard.Services;
using QualityDashboard.Hubs;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddSignalR();

// Register dashboard services
builder.Services.AddScoped<DashboardService>();
builder.Services.AddScoped<MetricsService>();
builder.Services.AddScoped<AgentService>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

app.MapRazorPages();
app.MapBlazorHub();
app.MapHub<MetricsHub>("/metrics-hub");
app.MapFallbackToPage("/_Host");

app.Run();
