module nli_0004
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_hop_down(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_hop_down

    select case(get_species(cell + (/0, -1, 0, default_a/)))
      case default
        nli_hop_down = 0; return
      case(empty)
        select case(get_species(cell + (/0, 0, 0, default_a/)))
          case default
            nli_hop_down = 0; return
          case(Au)
            nli_hop_down = hop_down; return
        end select
    end select

end function nli_hop_down

end module
