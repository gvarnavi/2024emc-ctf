import marimo

__generated_with = "0.8.2"
app = marimo.App()


@app.cell
def __(defocus_slider, mo, tabs):
    mo.vstack([tabs, defocus_slider.center()])
    return


@app.cell(hide_code=True)
async def __():
    # Imports
    import marimo as mo
    import numpy as np
    import os
    import sys

    from matplotlib import cm, colors as mcolors, pyplot as plt
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from colorspacious import cspace_convert

    if "pyodide" in sys.modules:
        import micropip
        await micropip.install("cmasher")

    import cmasher as cmr
    return (
        AnchoredSizeBar,
        cm,
        cmr,
        cspace_convert,
        make_axes_locatable,
        mcolors,
        micropip,
        mo,
        np,
        os,
        plt,
        sys,
    )


@app.cell(hide_code=True)
def __(energy2wavelength):
    q_probe = 1.0
    q_max = q_probe * 4
    sampling = 1 / q_max / 2

    energy = 300e3
    wavelength = energy2wavelength(energy)
    semiangle_mrad = q_probe * wavelength * 1e3
    return energy, q_max, q_probe, sampling, semiangle_mrad, wavelength


@app.cell(hide_code=True)
def __(gpts, np, q_probe, sampling):
    C1 = np.arange(0, 256, 4)
    qx = np.fft.fftfreq(gpts[0], sampling)
    qy = np.fft.fftfreq(gpts[1], sampling)
    q2 = qx[:, None] ** 2 + qy[None, :] ** 2
    q = np.sqrt(q2)

    # plotting coordinates
    inds_q = np.arange(gpts[0], gpts[0] // 2, -1) - 1
    defocus_norm = C1 * q_probe
    q_norm = qx[np.flip(inds_q)] / q_probe
    return C1, defocus_norm, inds_q, q, q2, q_norm, qx, qy


@app.cell(hide_code=True)
def __(np, q, q_probe, qx):
    # initial probe
    Psi_0 = np.sqrt(
        np.clip(
            (q_probe - q) / (qx[1] - qx[0]) + 0.5,
            0,
            1,
        ),
    )
    Psi_0 /= np.sqrt(np.sum(np.abs(Psi_0) ** 2))
    return Psi_0,


@app.cell(hide_code=True)
def __(C1, Psi_0, defocus_norm, inds_q, np, q, q2, q_probe, wavelength):
    # DPC
    Psi_dpc = Psi_0[None] * np.exp(
        -1j * np.pi * wavelength * defocus_norm[:, None, None] * q2[None]
    )
    CTF_dpc = np.fft.ifft2(np.abs(np.fft.fft2(Psi_dpc)) ** 2).real
    ctf_dpc = CTF_dpc[:, 0, inds_q]
    ctf_dpc = np.repeat(ctf_dpc, 2, axis=0)

    ERROR_rand_dpc = np.sqrt(2) / np.pi / q * q_probe
    ERROR_rand_dpc[0, 0] = np.inf
    error_rand_dpc = np.tile(ERROR_rand_dpc[0, inds_q], (C1.size, 1))
    error_rand_dpc = np.repeat(error_rand_dpc, 2, axis=0)
    return CTF_dpc, ERROR_rand_dpc, Psi_dpc, ctf_dpc, error_rand_dpc


@app.cell(hide_code=True)
def __(mo):
    defocus_slider = mo.ui.slider(
        start=0,
        stop=254,
        step=4,
        debounce=True,
        show_value=True,
        label=r"defocus (C1 * q$_\mathrm{probe}$)",
    )
    return defocus_slider,


@app.cell(hide_code=True)
def __(compute_figure, compute_ptycho_figure, defocus_index, mo):
    dpc = "Differential Phase Contrast (DPC)"
    parallax = "Tilt-Corrected BF-STEM (Parallax)"
    ptycho = "Gradient Descent Ptychography"

    tabs = mo.ui.tabs(
        {
            dpc: compute_figure(True, defocus_index),
            parallax: compute_figure(False, defocus_index),
            ptycho: compute_ptycho_figure(defocus_index),
        },
        lazy=False,
    )
    return dpc, parallax, ptycho, tabs


@app.cell(hide_code=True)
def __(
    CTF_dpc,
    CTF_parallax,
    Psi_dpc,
    cmr,
    ctf_dpc,
    ctf_parallax,
    error_rand_dpc,
    error_rand_parallax,
    make_axes_locatable,
    mcolors,
    np,
    plt,
    q_norm,
    show,
    show_complex,
):
    def compute_figure(dpc, defocus_index):
        fig = plt.figure(figsize=(9, 6.5))
        spec = fig.add_gridspec(6, 3, hspace=0)

        t = np.linspace(0, 1, 1024 + 1)
        t1 = ((np.sign(t - 0.5) * np.abs(2 * t - 1) ** 0.6) + 1) / 2
        cmap_ctf = mcolors.ListedColormap(plt.cm.RdBu_r(t1))

        ax1 = fig.add_subplot(spec[:3, 0])

        im1 = ax1.imshow(
            ctf_dpc if dpc else ctf_parallax,
            vmin=-1,
            vmax=1,
            cmap=cmap_ctf,
        )

        ax1.set_yticks(
            np.arange(0, 128 + 32, 32), labels=np.arange(0, 256 + 64, 64)
        )
        ax1.set_ylabel(r"defocus (C1 * q$_\mathrm{probe}$)")

        ax2 = fig.add_subplot(spec[:3, 1])

        t2 = t**0.25
        cmap_inv_error = mcolors.ListedColormap(cmr.nuclear(t2))

        im2 = ax2.imshow(
            1 / error_rand_dpc if dpc else 1 / error_rand_parallax,
            vmin=0,
            vmax=3,
            cmap=cmap_inv_error,
        )
        ax2.set_yticks([])

        t3 = t**0.5
        cmap_snr = mcolors.ListedColormap(cmr.arctic(t3))

        ax3 = fig.add_subplot(spec[:3, 2])

        im3 = ax3.imshow(
            (
                np.abs(ctf_dpc) / error_rand_dpc
                if dpc
                else np.abs(ctf_parallax) / error_rand_parallax
            ),
            vmin=0,
            vmax=1.5,
            cmap=cmap_snr,
        )
        ax3.set_yticks([])

        for ax, im, cbar_label in zip(
            [ax1, ax2, ax3],
            [im1, im2, im3],
            [
                "contrast transfer function",
                "inverse random error",
                "signal (|CTF|) / random error",
            ],
        ):
            ax.axhline(
                y=defocus_index * 2,
                color=[0.7, 0.2, 0.7],
                linestyle="--",
                linewidth=2,
            )
            ax.set_xticks(np.arange(0, 128 + 32, 32), labels=np.arange(0, 5, 1))
            ax.set_xlabel(r"q / q$_\mathrm{probe}$")
            ax.invert_yaxis()

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("top", size="5%", pad="2.5%")
            cb = plt.colorbar(im, cax=cax, orientation="horizontal")
            cax.xaxis.set_ticks_position("top")
            cax.set_xlabel(cbar_label)
            cax.xaxis.set_label_position("top")

        ax4 = fig.add_subplot(spec[3:, 0])

        show_complex(
            np.fft.fftshift(Psi_dpc[defocus_index]),
            figax=(fig, ax4),
            # ticks=False,
            cbar=False,
        )

        ax4.text(
            256 - 128,
            256 - 16,
            r"complex probe",
            horizontalalignment="center",
            color="white",
        )
        ax4.text(
            256 - 128,
            256 - 40,
            r"$\Psi(q) = A(q) \times \exp\left(-i \pi \lambda |q|^2 C_1 \right)$",
            horizontalalignment="center",
            color="white",
        )
        ax4.set_yticks(np.arange(0, 256 + 64, 64), labels=np.arange(-4, 6, 2))
        ax4.set_ylabel(r"q$_x$ / q$_\mathrm{probe}$")

        ax5 = fig.add_subplot(spec[3:, 1])

        show(
            (
                np.fft.fftshift(CTF_dpc[defocus_index])
                if dpc
                else np.fft.fftshift(CTF_parallax[defocus_index])
            ),
            figax=(fig, ax5),
            ticks=False,
            cbar=False,
            intensity_range=None,
            vmin=-1,
            vmax=1,
            cmap=cmap_ctf,
        )

        ax5.text(
            256 - 128,
            256 - 16,
            "probe autocorrelation" if dpc else "aperture autocorrelation",
            horizontalalignment="center",
        )

        ax5.text(
            256 - 128,
            256 - 40,
            (
                r"$\mathcal{F}^{-1}\left[\mathcal{F}\left[|\psi(q)|^2\right] \right]$"
                if dpc
                else r"$\mathcal{F}^{-1}\left[\mathcal{F}\left[|A(q)|^2\right] \right] \times \sin\left(-\pi \lambda |q|^2 C_1 \right)$"
            ),
            horizontalalignment="center",
        )

        for ax in [ax4, ax5]:
            ax.set_xticks(np.arange(0, 256 + 64, 64), labels=np.arange(-4, 6, 2))
            ax.set_xlabel(r"q$_y$ / q$_\mathrm{probe}$")
            ax.invert_yaxis()

        ax6 = fig.add_subplot(spec[3:, 2])
        # ax61 = fig.add_subplot(spec[3, 2])

        # ax61.plot(
        #     q_norm,
        #     ctf_dpc[2 * defocus_index] if dpc else ctf_parallax[2 * defocus_index],
        #     color=[1.0, 0.0, 1.0],
        #     linewidth=2,
        # )
        # ax61.set_xlabel("contrast transfer function")

        # ax62 = fig.add_subplot(spec[4, 2])

        # ax62.plot(
        #     q_norm,
        #     (
        #         1 / error_rand_dpc[2 * defocus_index]
        #         if dpc
        #         else 1 / error_rand_parallax[2 * defocus_index]
        #     ),
        #     color=[0.7, 0.2, 0.7],
        #     linewidth=2,
        # )

        # ax62.set_xlabel("inverse random error")

        # ax63 = fig.add_subplot(spec[5, 2])

        ax6.plot(
            q_norm,
            (
                np.abs(ctf_dpc[2 * defocus_index])
                / error_rand_dpc[2 * defocus_index]
                if dpc
                else np.abs(ctf_parallax[2 * defocus_index])
                / error_rand_parallax[2 * defocus_index]
            ),
            color=[0.7, 0.2, 0.7],
            linewidth=2,
        )

        ax6.set_xticks(np.arange(-4, 1, 1), labels=np.arange(0, 5, 1))
        ax6.set_xlabel(r"q / q$_\mathrm{probe}$")
        ax6.set_xlim([-4, 0])
        ax6.set_ylim([-0.1, 1.5])
        ax6.yaxis.tick_right()

        ax6.set_title("signal (|CTF|) / random error", fontsize=10)

        # for ax in [ax61, ax62]:
        #     ax.set_xticks([])
        #     ax.set_xlim([-4, 0])
        #     ax.yaxis.tick_right()

        # ax61.set_ylim([-1, 1])
        # ax62.set_ylim([-0.1, 8])

        spec.tight_layout(fig)
        
        fig.patch.set_facecolor('#dfdfd6')
        ax6.patch.set_facecolor('#dfdfd6')
        return fig
    return compute_figure,


@app.cell(hide_code=True)
def __(
    Psi_dpc,
    cmr,
    ctf_pty,
    error_pty,
    make_axes_locatable,
    mcolors,
    np,
    plt,
    q_norm,
    show_complex,
):
    def compute_ptycho_figure(defocus_index):
        fig = plt.figure(figsize=(9, 6.5))
        spec = fig.add_gridspec(6, 3, hspace=0)

        t = np.linspace(0, 1, 1024 + 1)
        t1 = ((np.sign(t - 0.5) * np.abs(2 * t - 1) ** 0.6) + 1) / 2
        cmap_ctf = mcolors.ListedColormap(plt.cm.RdBu_r(t1))

        ax1 = fig.add_subplot(spec[:3, 0])

        im1 = ax1.imshow(
            ctf_pty,
            vmin=-1,
            vmax=1,
            cmap=cmap_ctf,
        )

        ax1.set_yticks(
            np.arange(0, 128 + 32, 32), labels=np.arange(0, 256 + 64, 64)
        )
        ax1.set_ylabel(r"defocus (C1 * q$_\mathrm{probe}$)")
        ax1.set_xticks([])

        ax2 = fig.add_subplot(spec[:3, 1])

        t2 = t**0.25
        cmap_inv_error = mcolors.ListedColormap(cmr.nuclear(t2))

        im2 = ax2.imshow(
            1 / error_pty,
            vmin=0,
            vmax=3,
            cmap=cmap_inv_error,
        )
        ax2.set_yticks([])

        t3 = t**0.5
        cmap_snr = mcolors.ListedColormap(cmr.arctic(t3))

        ax3 = fig.add_subplot(spec[:3, 2])
        im3 = ax3.imshow(
            (np.abs(ctf_pty) / error_pty),
            vmin=0,
            vmax=1.5,
            cmap=cmap_snr,
        )

        ax3.set_yticks([])

        for ax, im, cbar_label in zip(
            [ax1, ax2, ax3],
            [im1, im2, im3],
            [
                "contrast transfer function",
                "inverse random error",
                "signal (|CTF|) / random error",
            ],
        ):
            ax.axhline(
                y=defocus_index * 2,
                color=[0.7, 0.2, 0.7],
                linestyle="--",
                linewidth=2,
            )
            ax.set_xticks(np.arange(0, 128 + 32, 32), labels=np.arange(0, 5, 1))
            ax.set_xlabel(r"q / q$_\mathrm{probe}$")
            ax.invert_yaxis()

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("top", size="5%", pad="2.5%")
            cb = plt.colorbar(im, cax=cax, orientation="horizontal")
            cax.xaxis.set_ticks_position("top")
            cax.set_xlabel(cbar_label)
            cax.xaxis.set_label_position("top")

        ax4 = fig.add_subplot(spec[3:, 0])

        show_complex(
            np.fft.fftshift(Psi_dpc[defocus_index]),
            figax=(fig, ax4),
            # ticks=False,
            cbar=False,
        )

        ax4.text(
            256 - 128,
            256 - 16,
            r"complex probe",
            horizontalalignment="center",
            color="white",
        )
        ax4.text(
            256 - 128,
            256 - 40,
            r"$\Psi(q) = A(q) \times \exp\left(-i \pi \lambda |q|^2 C_1 \right)$",
            horizontalalignment="center",
            color="white",
        )
        ax4.set_yticks(np.arange(0, 256 + 64, 64), labels=np.arange(-4, 6, 2))
        ax4.set_ylabel(r"q$_x$ / q$_\mathrm{probe}$")

        ax4.set_xticks(np.arange(0, 256 + 64, 64), labels=np.arange(-4, 6, 2))
        ax4.set_xlabel(r"q$_y$ / q$_\mathrm{probe}$")
        ax4.invert_yaxis()

        ax6 = fig.add_subplot(spec[3:, 2])
        # ax61 = fig.add_subplot(spec[3, 2])

        # ax61.plot(
        #     q_norm,
        #     ctf_pty[defocus_index],
        #     color=[1.0, 0.0, 1.0],
        #     linewidth=2,
        # )
        # ax61.set_xlabel("contrast transfer function")

        # ax62 = fig.add_subplot(spec[4, 2])

        # ax62.plot(
        #     q_norm,
        #     (1 / error_pty[defocus_index]),
        #     color=[0.7, 0.2, 0.7],
        #     linewidth=2,
        # )

        # ax62.set_xlabel("inverse random error")

        # ax63 = fig.add_subplot(spec[5, 2])

        ax6.plot(
            q_norm,
            np.abs(ctf_pty[defocus_index]) / error_pty[defocus_index],
            color=[0.7, 0.2, 0.7],
            linewidth=2,
        )

        ax6.set_xticks(np.arange(-4, 1, 1), labels=np.arange(0, 5, 1))
        ax6.set_xlabel(r"q / q$_\mathrm{probe}$")
        ax6.set_xlim([-4, 0])
        ax6.set_ylim([-0.1, 0.5])
        ax6.yaxis.tick_right()

        ax6.set_title("signal (|CTF|) / random error", fontsize=10)

        # for ax in [ax61, ax62]:
        #     ax.set_xticks([])
        #     ax.set_xlim([-4, 0])
        #     ax.yaxis.tick_right()

        # ax61.set_ylim([0.9, 1.1])
        # ax62.set_ylim([-0.1, 2])

        spec.tight_layout(fig)

        fig.patch.set_facecolor('#dfdfd6')
        ax6.patch.set_facecolor('#dfdfd6')
        return fig
    return compute_ptycho_figure,


@app.cell(hide_code=True)
def __(Psi_0, defocus_norm, error_rand_dpc, inds_q, np, q2, wavelength):
    # Parallax
    CTF_parallax = np.fft.ifft2(np.abs(np.fft.fft2(Psi_0)) ** 2).real
    CTF_parallax = CTF_parallax * np.sin(
        np.pi * wavelength * defocus_norm[:, None, None] * q2[None]
    )

    ctf_parallax = CTF_parallax[:, 0, inds_q]
    ctf_parallax = np.repeat(ctf_parallax, 2, axis=0)

    error_rand_parallax = np.full_like(error_rand_dpc, np.sqrt(2) / np.pi)
    return CTF_parallax, ctf_parallax, error_rand_parallax


@app.cell(hide_code=True)
def __():
    gpts = [256, 256]
    return gpts,


@app.cell(hide_code=True)
def __(defocus_slider):
    defocus_index = defocus_slider.value // 4
    return defocus_index,


@app.cell(hide_code=True)
def __(
    AnchoredSizeBar,
    cm,
    cspace_convert,
    make_axes_locatable,
    mcolors,
    np,
    plt,
):
    # Plotting


    def return_scaled_histogram(
        array,
        vmin=None,
        vmax=None,
    ):
        if np.isclose(np.max(array), np.min(array)):
            if vmin is None:
                vmin = 0
            if vmax is None:
                vmax = np.max(array)
        else:
            if vmin is None:
                vmin = 0.02
            if vmax is None:
                vmax = 0.98

            vals = np.sort(array[~np.isnan(array)])
            ind_vmin = np.round((vals.shape[0] - 1) * vmin).astype("int")
            ind_vmax = np.round((vals.shape[0] - 1) * vmax).astype("int")
            ind_vmin = np.max([0, ind_vmin])
            ind_vmax = np.min([len(vals) - 1, ind_vmax])
            vmin = vals[ind_vmin]
            vmax = vals[ind_vmax]

        array = np.where(array < vmin, vmin, array)
        array = np.where(array > vmax, vmax, array)

        return array, vmin, vmax


    def Complex2RGB(
        complex_data, vmin=None, vmax=None, power=None, chroma_boost=1
    ):
        """ """
        amp = np.abs(complex_data)
        phase = np.angle(complex_data)

        if power is not None:
            amp = amp**power

        amp, vmin, vmax = return_scaled_histogram(amp, vmin, vmax)
        amp = ((amp - vmin) / vmax).clip(1e-16, 1)

        J = amp * 61.5  # Note we restrict luminance to the monotonic chroma cutoff
        C = np.minimum(chroma_boost * 98 * J / 123, 110)
        h = np.rad2deg(phase) + 180

        JCh = np.stack((J, C, h), axis=-1)
        rgb = cspace_convert(JCh, "JCh", "sRGB1").clip(0, 1)

        return rgb


    def add_scalebar(
        ax, length, sampling, units, color="white", size_vertical=1, pad=0.5
    ):
        """ """
        bar = AnchoredSizeBar(
            ax.transData,
            length,
            f"{sampling*length:.2f} {units}",
            "lower right",
            pad=pad,
            color=color,
            frameon=False,
            label_top=True,
            size_vertical=size_vertical,
        )
        ax.add_artist(bar)
        return ax


    def add_colorbar_arg(cax, chroma_boost=1, c=49, j=61.5):
        """
        cax                 : axis to add cbar to
        chroma_boost (float): boosts chroma for higher-contrast (~1-2.25)
        c (float)           : constant chroma value
        j (float)           : constant luminance value
        """

        h = np.linspace(0, 360, 256, endpoint=False)
        J = np.full_like(h, j)
        C = np.full_like(h, np.minimum(c * chroma_boost, 110))
        JCh = np.stack((J, C, h), axis=-1)
        rgb_vals = cspace_convert(JCh, "JCh", "sRGB1").clip(0, 1)
        newcmp = mcolors.ListedColormap(rgb_vals)
        norm = mcolors.Normalize(vmin=-np.pi, vmax=np.pi)

        cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=newcmp), cax=cax)

        cb.set_label("arg", rotation=0, ha="center", va="bottom")
        cb.ax.yaxis.set_label_coords(0.5, 1.01)
        cb.set_ticks(np.array([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]))
        cb.set_ticklabels(
            [r"$-\pi$", r"$-\dfrac{\pi}{2}$", "$0$", r"$\dfrac{\pi}{2}$", r"$\pi$"]
        )


    def show_complex(
        complex_data,
        figax=None,
        vmin=None,
        vmax=None,
        power=None,
        ticks=True,
        chroma_boost=1,
        cbar=True,
        **kwargs,
    ):
        """ """
        rgb = Complex2RGB(
            complex_data, vmin, vmax, power=power, chroma_boost=chroma_boost
        )

        figsize = kwargs.pop("figsize", (6, 6))
        if figax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = figax

        ax.imshow(rgb, interpolation=None, **kwargs)

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            add_colorbar_arg(ax_cb, chroma_boost=chroma_boost)

        if ticks is False:
            ax.set_xticks([])
            ax.set_yticks([])

        return ax


    def show(
        array,
        figax=None,
        vmin=None,
        vmax=None,
        power=None,
        ticks=True,
        cbar=True,
        cmap="gray",
        intensity_range="ordered",
        **kwargs,
    ):
        """ """

        if power is not None:
            array = array**power

        if intensity_range == "ordered" or intensity_range == "centered":
            array, vmin, vmax = return_scaled_histogram(array, vmin, vmax)

        if intensity_range == "centered":
            vmax = np.maximum(np.abs(vmin), np.abs(vmax))
            vmin = -vmax

        figsize = kwargs.pop("figsize", (6, 6))
        if figax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = figax

        im = ax.imshow(
            array, vmin=vmin, vmax=vmax, cmap=cmap, interpolation=None, **kwargs
        )

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            cb = plt.colorbar(im, cax=ax_cb)

        if ticks is False:
            ax.set_xticks([])
            ax.set_yticks([])

        return ax
    return (
        Complex2RGB,
        add_colorbar_arg,
        add_scalebar,
        return_scaled_histogram,
        show,
        show_complex,
    )


@app.cell(hide_code=True)
def __(np):
    # Complex Probes Utilities
    def energy2wavelength(energy):
        """ """
        hplanck = 6.62607e-34
        c = 299792458.0
        me = 9.1093856e-31
        e = 1.6021766208e-19

        return (
            hplanck
            * c
            / np.sqrt(energy * (2 * me * c**2 / e + energy))
            / e
            * 1.0e10
        )


    class ComplexProbe:
        """ """

        # fmt: off
        _polar_symbols = (
            "C10", "C12", "phi12",
            "C21", "phi21", "C23", "phi23",
            "C30", "C32", "phi32", "C34", "phi34",
            "C41", "phi41", "C43", "phi43", "C45", "phi45",
            "C50", "C52", "phi52", "C54", "phi54", "C56", "phi56",
        )

        _polar_aliases = {
            "defocus": "C10", "astigmatism": "C12", "astigmatism_angle": "phi12",
            "coma": "C21", "coma_angle": "phi21",
            "Cs": "C30",
            "C5": "C50",
        }
        # fmt: on

        def __init__(
            self,
            energy,
            gpts,
            sampling,
            semiangle_cutoff,
            soft_aperture=True,
            parameters={},
            **kwargs,
        ):
            self._energy = energy
            self._gpts = gpts
            self._sampling = sampling
            self._semiangle_cutoff = semiangle_cutoff
            self._soft_aperture = soft_aperture

            self._parameters = dict(
                zip(self._polar_symbols, [0.0] * len(self._polar_symbols))
            )
            parameters.update(kwargs)
            self.set_parameters(parameters)
            self._wavelength = energy2wavelength(self._energy)

        def set_parameters(self, parameters):
            """ """
            for symbol, value in parameters.items():
                if symbol in self._parameters.keys():
                    self._parameters[symbol] = value

                elif symbol == "defocus":
                    self._parameters[self._polar_aliases[symbol]] = -value

                elif symbol in self._polar_aliases.keys():
                    self._parameters[self._polar_aliases[symbol]] = value

                else:
                    raise ValueError(
                        "{} not a recognized parameter".format(symbol)
                    )

            return parameters

        def get_spatial_frequencies(self):
            return tuple(
                np.fft.fftfreq(n, d) for n, d in zip(self._gpts, self._sampling)
            )

        def get_scattering_angles(self):
            kx, ky = self.get_spatial_frequencies()
            kx, ky = kx * self._wavelength, ky * self._wavelength
            alpha = np.sqrt(kx[:, None] ** 2 + ky[None, :] ** 2)
            phi = np.arctan2(ky[None, :], kx[:, None])
            return alpha, phi

        def hard_aperture(self, alpha, semiangle_cutoff):
            return alpha <= semiangle_cutoff

        def soft_aperture(self, alpha, semiangle_cutoff, angular_sampling):
            denominator = (
                np.sqrt(angular_sampling[0] ** 2 + angular_sampling[1] ** 2) * 1e-3
            )
            return np.clip((semiangle_cutoff - alpha) / denominator + 0.5, 0, 1)

        def evaluate_aperture(self, alpha, phi):
            if self._soft_aperture:
                return self.soft_aperture(
                    alpha, self._semiangle_cutoff * 1e-3, self.angular_sampling
                )
            else:
                return self.hard_aperture(alpha, self._semiangle_cutoff * 1e-3)

        def evaluate_chi(self, alpha, phi):
            p = self._parameters

            alpha2 = alpha**2

            array = np.zeros_like(alpha)
            if any([p[symbol] != 0.0 for symbol in ("C10", "C12", "phi12")]):
                array += (
                    1
                    / 2
                    * alpha2
                    * (p["C10"] + p["C12"] * np.cos(2 * (phi - p["phi12"])))
                )

            if any(
                [p[symbol] != 0.0 for symbol in ("C21", "phi21", "C23", "phi23")]
            ):
                array += (
                    1
                    / 3
                    * alpha2
                    * alpha
                    * (
                        p["C21"] * np.cos(phi - p["phi21"])
                        + p["C23"] * np.cos(3 * (phi - p["phi23"]))
                    )
                )

            if any(
                [
                    p[symbol] != 0.0
                    for symbol in ("C30", "C32", "phi32", "C34", "phi34")
                ]
            ):
                array += (
                    1
                    / 4
                    * alpha2**2
                    * (
                        p["C30"]
                        + p["C32"] * np.cos(2 * (phi - p["phi32"]))
                        + p["C34"] * np.cos(4 * (phi - p["phi34"]))
                    )
                )

            if any(
                [
                    p[symbol] != 0.0
                    for symbol in ("C41", "phi41", "C43", "phi43", "C45", "phi41")
                ]
            ):
                array += (
                    1
                    / 5
                    * alpha2**2
                    * alpha
                    * (
                        p["C41"] * np.cos((phi - p["phi41"]))
                        + p["C43"] * np.cos(3 * (phi - p["phi43"]))
                        + p["C45"] * np.cos(5 * (phi - p["phi45"]))
                    )
                )

            if any(
                [
                    p[symbol] != 0.0
                    for symbol in (
                        "C50",
                        "C52",
                        "phi52",
                        "C54",
                        "phi54",
                        "C56",
                        "phi56",
                    )
                ]
            ):
                array += (
                    1
                    / 6
                    * alpha2**3
                    * (
                        p["C50"]
                        + p["C52"] * np.cos(2 * (phi - p["phi52"]))
                        + p["C54"] * np.cos(4 * (phi - p["phi54"]))
                        + p["C56"] * np.cos(6 * (phi - p["phi56"]))
                    )
                )

            array = 2 * np.pi / self._wavelength * array
            return array

        def evaluate_aberrations(self, alpha, phi):
            self._chi = self.evaluate_chi(alpha, phi)
            return np.exp(-1.0j * self._chi)

        def evaluate_ctf(self):
            alpha, phi = self.get_scattering_angles()
            array = self.evaluate_aberrations(alpha, phi)
            self._aperture = self.evaluate_aperture(alpha, phi)
            return array * self._aperture

        def build(self):
            array_fourier = self.evaluate_ctf()
            array_fourier /= np.sqrt(np.sum(np.abs(array_fourier) ** 2))
            self._array_fourier = array_fourier
            self._array = np.fft.ifft2(self._array_fourier)
            return self

        @property
        def sampling(self):
            return self._sampling

        @property
        def reciprocal_space_sampling(self):
            return tuple(1 / (n * s) for n, s in zip(self._gpts, self._sampling))

        @property
        def angular_sampling(self):
            return tuple(
                dk * self._wavelength * 1e3
                for dk in self.reciprocal_space_sampling
            )
    return ComplexProbe, energy2wavelength


@app.cell(hide_code=True)
async def __(__file__, np, os, sys):
    if "pyodide" in sys.modules:
        from pyodide.http import pyfetch

        async def download_remote_file(url, filename, overwrite=False):
            if not os.path.isfile(filename) or overwrite:
                # print(f"Downloading file to {filename}")
                response = await pyfetch(url)
                if response.status == 200:
                    with open(filename, "wb") as f:
                        f.write(await response.bytes())
        
        
        file_url = "https://raw.githubusercontent.com/gvarnavi/py4dstem-phase-retrieval-paper-notebooks/main/data/"
        ptycho_ctf_file = "ctf_pty.npy"
        ptycho_error_file = "error_pty.npy"
        
        await download_remote_file(file_url + ptycho_ctf_file, ptycho_ctf_file)
        await download_remote_file(file_url + ptycho_error_file, ptycho_error_file)

    else:
        file_url = os.path.dirname(os.path.realpath(__file__)) + "/data/"
        ptycho_ctf_file = file_url+"ctf_pty.npy"
        ptycho_error_file = file_url+"error_pty.npy"

    ctf_pty = np.load(ptycho_ctf_file)
    error_pty = np.load(ptycho_error_file) * np.sqrt(1e4 / 128)
    error_pty[:, 0] = np.inf

    ctf_pty = np.repeat(ctf_pty, 2, axis=0)
    error_pty = np.repeat(error_pty, 2, axis=0)
    return (
        ctf_pty,
        download_remote_file,
        error_pty,
        file_url,
        ptycho_ctf_file,
        ptycho_error_file,
        pyfetch,
    )


if __name__ == "__main__":
    app.run()
