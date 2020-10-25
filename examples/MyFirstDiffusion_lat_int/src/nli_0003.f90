module nli_0003
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_CO_diffusion_hollow2_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_CO_diffusion_hollow2_right

    select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow2/)))
      case default
        nli_CO_diffusion_hollow2_right = 0; return
      case(CO)
        select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow3/)))
          case default
            nli_CO_diffusion_hollow2_right = 0; return
          case(empty)
            nli_CO_diffusion_hollow2_right = CO_diffusion_hollow2_right; return
        end select
    end select

end function nli_CO_diffusion_hollow2_right

end module
